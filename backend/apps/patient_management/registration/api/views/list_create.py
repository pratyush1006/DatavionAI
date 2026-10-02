"""
API views for listing and creating patient registrations.

Architecture:
    GET
        Selector driven.

    POST
        Workflow driven.

The API layer owns HTTP concerns only. Authorization is delegated to
the RBAC permission layer, reads to selectors, and mutations to workflows.
"""

from __future__ import annotations

from typing import Any, Final, cast

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.patient_management.registration.api.filters import (
    PatientRegistrationFilter,
)
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationCreateSerializer,
    PatientRegistrationDetailSerializer,
    PatientRegistrationListSerializer,
)
from apps.patient_management.registration.models import PatientRegistration
from apps.patient_management.registration.permissions import (
    CanCreateRegistration,
    CanViewRegistration,
)
from apps.patient_management.registration.selectors import (
    get_registration_by_uuid,
    list_organization_registrations,
    list_patient_registrations,
)
from apps.patient_management.registration.workflows import (
    RegistrationCreationRequest,
    RegistrationCreationWorkflow,
)
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

REGISTRATION_TAG: Final[tuple[str, ...]] = ("Patient Registrations",)


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List or create patient registrations.

    GET:
        Organization-scoped selector.

    POST:
        Registration creation workflow.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewRegistration,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateRegistration,
        ),
    }

    serializer_classes = {
        "GET": PatientRegistrationListSerializer,
        "POST": PatientRegistrationCreateSerializer,
    }

    detail_serializer_class = PatientRegistrationDetailSerializer

    create_workflow = RegistrationCreationWorkflow

    create_success_message = "Patient registration created successfully."

    filter_backends = (  # type: ignore[misc]
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = PatientRegistrationFilter

    search_fields = (
        "registration_number",
        "patient__first_name",
        "patient__last_name",
        "patient__mrn",
    )

    ordering_fields = (
        "registration_datetime",
        "registration_number",
        "registration_status",
        "registration_type",
        "registration_source",
        "priority",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-registration_datetime",
        "-created_at",
    )

    def _resolve_organization(self):
        """
        Resolve the organization from the authenticated request context.

        Resolution order:
            1. current_organization
            2. request.organization
            3. user's first organization role

        Organization is always resolved server-side and is never accepted
        as client-controlled input.
        """
        organization = self.current_organization

        if organization is not None:
            return organization

        organization = getattr(
            self.request,
            "organization",
            None,
        )

        if organization is not None:
            return organization

        user = self.request.user

        organization_role = user.organization_roles.select_related(
            "organization"
        ).first()

        if organization_role is not None:
            return organization_role.organization

        return None

    def get_queryset(self) -> QuerySet[PatientRegistration]:
        """
        Return registrations scoped to the current organization.

        No unrestricted registration queryset is exposed through the API.
        """
        organization = self._resolve_organization()

        if organization is None:
            return cast(
                QuerySet[PatientRegistration],
                PatientRegistration.objects.none(),
            )

        patient_id = self.request.query_params.get("patient")

        if patient_id:
            return list_patient_registrations(
                patient_id=patient_id,
                organization=organization,
            )

        return list_organization_registrations(
            organization=organization,
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> RegistrationCreationRequest:
        """
        Build the creation workflow request.

        Organization is resolved from the authenticated request context
        and is intentionally not accepted as client-controlled input.

        The patient comes from validated serializer data. The workflow
        performs the authoritative organization-scoped patient lookup.
        """
        organization = self._resolve_organization()

        if organization is None:
            raise ValueError(
                "Organization context is required to create a registration."
            )

        patient = validated_data["patient"]

        return RegistrationCreationRequest(
            organization_id=organization.pk,
            patient_id=patient.pk,
            data={
                key: value for key, value in validated_data.items() if key != "patient"
            },
        )

    def resolve_workflow_created_instance(
        self,
        result: Any,
    ) -> PatientRegistration | None:
        """
        Resolve the created registration from the workflow result.

        The workflow returns the registration UUID. The instance is then
        resolved through the organization-scoped selector so the API never
        falls back to an unrestricted model lookup.
        """
        data = result.data

        if data is None:
            return None

        registration_id = getattr(
            data,
            "registration_id",
            None,
        )

        if registration_id is None:
            return None

        organization = self._resolve_organization()

        if organization is None:
            return None

        return get_registration_by_uuid(
            uuid=registration_id,
            organization=organization,
        )


__all__ = ("PatientRegistrationListCreateAPIView",)
