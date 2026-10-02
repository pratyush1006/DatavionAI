"""
API views for listing and creating allergies.
"""

from __future__ import annotations

from typing import Final
from uuid import uuid4

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.allergies.api.serializers import (
    AllergyCreateSerializer,
    AllergyDetailSerializer,
    AllergyListSerializer,
)
from apps.clinical.allergies.models import Allergy
from apps.clinical.allergies.permissions import (
    CanCreateAllergy,
    CanViewAllergy,
)
from apps.clinical.allergies.selectors import get_allergies
from apps.clinical.allergies.services import create_allergy
from apps.clinical.allergies.workflows import (
    AllergyCreationRequest,
    AllergyCreationWorkflow,
)
from apps.clinical.encounters.models import Encounter
from apps.common.api.base_generics import BaseListCreateAPIView
from apps.core.workflows import WorkflowContext
from apps.platform.organizations.models import Organization

ALLERGY_TAG: Final[tuple[str, ...]] = ("Allergies",)


@extend_schema(tags=ALLERGY_TAG)
class AllergyListCreateAPIView(BaseListCreateAPIView):
    create_workflow = AllergyCreationWorkflow
    """
    List existing allergies or create a new allergy.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAllergy,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateAllergy,
        ),
    }

    serializer_classes = {
        "GET": AllergyListSerializer,
        "POST": AllergyCreateSerializer,
    }

    detail_serializer_class = AllergyDetailSerializer

    create_service = create_allergy

    create_success_message = "Allergy created successfully."

    search_fields = (
        "allergen",
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "allergen",
        "category",
        "severity",
        "status",
        "created_at",
    )

    filterset_fields = (
        "category",
        "severity",
        "status",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Allergy]:
        """
        Return the allergies queryset.
        """

        return get_allergies()


__all__ = [
    "AllergyListCreateAPIView",
]


def _allergy_create_workflow_context(self):
    user = self.request.user
    tenant = self.current_tenant
    organization = self.current_organization
    if organization is None:
        organization_id = self.request.data.get(
            "organization"
        ) or self.request.data.get("organization_id")
        if organization_id:
            organization = Organization.objects.select_related("tenant").get(
                pk=organization_id
            )
            self._workflow_organization_id = organization.id
    if tenant is None and organization is not None:
        tenant = organization.tenant
    if tenant is None:
        raise RuntimeError("Tenant context is required.")
    return WorkflowContext(
        tenant_id=tenant.id,
        actor_id=user.id,
        correlation_id=str(uuid4()),
        request_id=str(uuid4()),
        workflow_name="allergy.create",
    )


AllergyListCreateAPIView.get_workflow_context = _allergy_create_workflow_context


def _allergy_build_workflow_request(self, validated_data):
    organization = validated_data["organization"]
    patient = validated_data["patient"]
    provider = validated_data.get("provider")
    encounter = validated_data.get("encounter")
    if encounter is None:
        encounter = self.request.data.get("encounter") or self.request.data.get(
            "encounter_id"
        )
    if encounter is None:
        raise ValueError("Encounter is required to create an allergy.")
    if not hasattr(encounter, "id"):
        encounter = Encounter.objects.get(pk=encounter, organization_id=organization.id)
    elif getattr(encounter, "organization_id", organization.id) != organization.id:
        raise ValueError("Encounter does not belong to the selected organization.")
    self._workflow_organization_id = organization.id
    return AllergyCreationRequest(
        organization_id=organization.id,
        patient_id=patient.id,
        provider_id=getattr(provider, "id", None),
        encounter_id=encounter.id,
        data=dict(validated_data),
    )


AllergyListCreateAPIView.build_workflow_request = _allergy_build_workflow_request


def _allergy_resolve_workflow_created_instance(self, workflow_result, *args, **kwargs):
    # Prefer the concrete object returned by the Allergy workflow.
    data = getattr(workflow_result, "data", workflow_result)
    if isinstance(data, Allergy):
        return data
    if isinstance(data, dict):
        for key in ("allergy", "instance", "object"):
            instance = data.get(key)
            if isinstance(instance, Allergy):
                return instance
        for key in ("id", "allergy_id", "object_id"):
            object_id = data.get(key)
            if object_id is not None:
                try:
                    return self.get_queryset().get(pk=object_id)
                except Allergy.DoesNotExist:
                    pass
    object_id = getattr(data, "id", None)
    if object_id is not None:
        try:
            return self.get_queryset().get(pk=object_id)
        except Allergy.DoesNotExist:
            pass

    # The common workflow mixin may normalize WorkflowResult.data into a
    # lightweight identifier that is not the Allergy primary key. Resolve the
    # newly-created row using the same tenant/patient/request contract instead
    # of weakening the model or changing shared infrastructure.
    organization = self.current_organization
    if organization is None:
        organization_id = self.request.data.get(
            "organization"
        ) or self.request.data.get("organization_id")
    else:
        organization_id = organization.id
    patient_id = self.request.data.get("patient") or self.request.data.get("patient_id")
    if organization_id is not None and patient_id is not None:
        queryset = Allergy.objects.filter(
            organization_id=organization_id,
            patient_id=patient_id,
        ).order_by("-created_at", "-id")
        instance = queryset.first()
        if instance is not None:
            return instance
    raise RuntimeError(
        "Allergy creation workflow did not return the created Allergy instance."
    )


AllergyListCreateAPIView.resolve_workflow_created_instance = (
    _allergy_resolve_workflow_created_instance
)
