"""
API views for listing and creating vitals.
"""

from __future__ import annotations

from typing import Final
from uuid import uuid4

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.vitals.api.serializers import (
    VitalCreateSerializer,
    VitalDetailSerializer,
    VitalListSerializer,
)
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.permissions import (
    CanCreateVital,
    CanViewVital,
)
from apps.clinical.vitals.selectors import get_vitals
from apps.clinical.vitals.services import create_vital
from apps.clinical.vitals.workflows import VitalCreationRequest, VitalCreationWorkflow
from apps.common.api.base_generics import BaseListCreateAPIView
from apps.core.workflows import WorkflowContext
from apps.platform.organizations.models import Organization

VITAL_TAG: Final[tuple[str, ...]] = ("Vitals",)


@extend_schema(tags=VITAL_TAG)
class VitalListCreateAPIView(BaseListCreateAPIView):
    def resolve_workflow_created_instance(self, workflow_result):
        data = getattr(workflow_result, "data", None)
        if hasattr(data, "pk"):
            return data
        if isinstance(data, dict):
            instance = data.get("instance") or data.get("object")
            if hasattr(instance, "pk"):
                return instance
        return super().resolve_workflow_created_instance(workflow_result)

    create_workflow = VitalCreationWorkflow
    """
    List existing vitals or create a new vital record.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewVital,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateVital,
        ),
    }

    serializer_classes = {
        "GET": VitalListSerializer,
        "POST": VitalCreateSerializer,
    }

    detail_serializer_class = VitalDetailSerializer

    create_service = create_vital

    create_success_message = "Vital created successfully."

    search_fields = (
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
        "encounter__encounter_number",
    )

    ordering = ("-recorded_at",)

    ordering_fields = (
        "recorded_at",
        "status",
        "temperature",
        "pulse",
        "oxygen_saturation",
        "created_at",
    )

    filterset_fields = (
        "status",
        "temperature_unit",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Vital]:
        """
        Return the vitals queryset.
        """

        return get_vitals()


__all__ = [
    "VitalListCreateAPIView",
]


def _vital_create_workflow_context(self):
    user = self.request.user
    tenant_id = getattr(user, "tenant_id", None)
    organization_id = self.request.data.get("organization") or self.request.data.get(
        "organization_id"
    )
    if tenant_id is None and organization_id:
        tenant_id = (
            Organization.objects.only("tenant_id").get(pk=organization_id).tenant_id
        )
    if tenant_id is None:
        raise RuntimeError("Tenant context is required.")
    return WorkflowContext(
        tenant_id=tenant_id,
        actor_id=user.id,
        correlation_id=str(uuid4()),
        request_id=str(uuid4()),
        workflow_name="vital.create",
    )


VitalListCreateAPIView.get_workflow_context = _vital_create_workflow_context


def _vital_build_workflow_request(self, validated_data):
    organization = validated_data["organization"]
    patient = validated_data["patient"]
    provider = validated_data["provider"]
    encounter = validated_data.get("encounter")
    return VitalCreationRequest(
        organization_id=organization.id,
        patient_id=patient.id,
        provider_id=provider.id,
        encounter_id=getattr(encounter, "id", None),
        data=dict(validated_data),
    )


VitalListCreateAPIView.build_workflow_request = _vital_build_workflow_request
