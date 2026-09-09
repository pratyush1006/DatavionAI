"""
API views for listing and creating Patient Relationships.

Architecture
------------
GET
    Selector-driven.

POST
    Workflow-driven.
"""

from __future__ import annotations

from typing import Any, Final

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.patient_management.relationships.api.filters import (
    PatientRelationshipFilter,
)
from apps.patient_management.relationships.api.serializers import (
    PatientRelationshipCreateSerializer,
    PatientRelationshipDetailSerializer,
    PatientRelationshipListSerializer,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)
from apps.patient_management.relationships.selectors import (
    PatientRelationshipSelector,
)
from apps.patient_management.relationships.workflows import (
    PatientRelationshipCreationRequest,
    PatientRelationshipCreationWorkflow,
)

RELATIONSHIP_TAG: Final[tuple[str, ...]] = ("Patient Relationships",)


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List or create Patient Relationships.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated,),
        "POST": (IsAuthenticated,),
    }

    serializer_classes = {
        "GET": PatientRelationshipListSerializer,
        "POST": PatientRelationshipCreateSerializer,
    }

    detail_serializer_class = PatientRelationshipDetailSerializer

    create_workflow = PatientRelationshipCreationWorkflow

    create_success_message = "Patient relationship created successfully."

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = PatientRelationshipFilter

    search_fields = (
        "relationship_name",
        "patient__first_name",
        "patient__last_name",
        "related_patient__first_name",
        "related_patient__last_name",
    )

    ordering_fields = (
        "relationship_type",
        "status",
        "verification_status",
        "effective_from",
        "effective_to",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-is_primary",
        "-created_at",
    )

    def get_queryset(
        self,
    ) -> QuerySet[PatientRelationship]:
        """
        Return only relationships belonging to the current organization.
        """
        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            user = self.request.user

            organization_roles = getattr(
                user,
                "organization_roles",
                None,
            )

            if organization_roles is not None:
                organization_role = organization_roles.select_related(
                    "organization"
                ).first()

                if organization_role is not None:
                    organization = organization_role.organization

        if organization is None:
            return PatientRelationship.objects.none()

        patient_id = self.request.query_params.get(
            "patient",
        )

        if patient_id:
            return PatientRelationshipSelector.for_patient(
                organization=organization,
                patient_id=patient_id,
            )

        return PatientRelationshipSelector.list(
            organization=organization,
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> PatientRelationshipCreationRequest:
        """
        Build the creation workflow request.

        Organization is always taken from trusted request context.
        """
        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            user = self.request.user

            organization_roles = getattr(
                user,
                "organization_roles",
                None,
            )

            if organization_roles is not None:
                organization_role = organization_roles.select_related(
                    "organization"
                ).first()

                if organization_role is not None:
                    organization = organization_role.organization

        if organization is None:
            raise ValueError(
                "Organization context is required to create a patient relationship."
            )

        patient = validated_data["patient"]

        return PatientRelationshipCreationRequest(
            organization_id=organization.pk,
            patient_id=patient.pk,
            data={
                key: value for key, value in validated_data.items() if key != "patient"
            },
        )


__all__ = ("PatientRelationshipListCreateAPIView",)
