"""
API views for listing and creating patient identifiers.

Architecture:

GET
    Selector driven

POST
    Workflow driven
"""

from __future__ import annotations

from typing import Any, Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.patient_management.identifiers.api.serializers import (
    PatientIdentifierCreateSerializer,
    PatientIdentifierDetailSerializer,
    PatientIdentifierListSerializer,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.permissions import (
    CanCreateIdentifier,
    CanViewIdentifier,
)
from apps.patient_management.identifiers.selectors import (
    get_patient_identifiers,
)
from apps.patient_management.identifiers.workflows import (
    IdentifierCreationRequest,
    IdentifierCreationWorkflow,
)

IDENTIFIER_TAG: Final[tuple[str, ...]] = ("Patient Identifiers",)


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List or create patient identifiers.

    GET is selector driven.

    POST is workflow driven.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewIdentifier,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateIdentifier,
        ),
    }

    serializer_classes = {
        "GET": PatientIdentifierListSerializer,
        "POST": PatientIdentifierCreateSerializer,
    }

    detail_serializer_class = PatientIdentifierDetailSerializer

    create_workflow = IdentifierCreationWorkflow

    create_success_message = "Patient identifier created successfully."

    search_fields = (
        "identifier_type",
        "display_value",
        "issuing_authority",
    )

    ordering = (
        "-is_primary",
        "priority",
        "identifier_type",
        "created_at",
    )

    ordering_fields = (
        "identifier_type",
        "priority",
        "status",
        "verification_status",
        "issued_at",
        "expires_at",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "patient",
        "identifier_type",
        "status",
        "verification_status",
        "source",
        "priority",
        "is_primary",
    )

    def get_queryset(self) -> QuerySet[PatientIdentifier]:
        """
        Return identifiers scoped to the current organization.
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

            organization_role = user.organization_roles.select_related(
                "organization"
            ).first()

            if organization_role is not None:
                organization = organization_role.organization

        if organization is None:
            return PatientIdentifier.objects.none()

        patient_id = self.request.query_params.get("patient")

        if patient_id:
            return get_patient_identifiers(
                organization=organization,
                patient_id=patient_id,
            )

        return (
            PatientIdentifier.objects.filter(
                organization_id=organization.pk,
            )
            .with_relations()
            .ordered()
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> IdentifierCreationRequest:
        """
        Build the Patient Identifier creation workflow request.
        """
        organization = validated_data["organization"]
        patient = validated_data["patient"]

        return IdentifierCreationRequest(
            organization_id=organization.pk,
            patient_id=patient.pk,
            data={
                key: value
                for key, value in validated_data.items()
                if key
                not in {
                    "organization",
                    "patient",
                }
            },
        )

    def resolve_workflow_created_instance(
        self,
        result: Any,
    ) -> PatientIdentifier | None:
        """
        Resolve the created PatientIdentifier from the workflow DTO.

        The shared workflow mixin does not know about identifier_id, so
        this bounded context provides its own resolution.
        """
        data = result.data

        if data is None:
            return None

        identifier_id = getattr(
            data,
            "identifier_id",
            None,
        )

        if identifier_id is None:
            return None

        return self.get_queryset().get(
            pk=identifier_id,
        )


__all__ = ("PatientIdentifierListCreateAPIView",)
