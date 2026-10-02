"""
API views for retrieving, updating, and deleting patient registrations.

Architecture
------------

GET
    Organization-scoped selector.

PUT/PATCH
    Workflow driven.

DELETE
    Workflow driven.

The API layer owns HTTP concerns only. Authorization is delegated to the
RBAC permission layer, reads to selectors, and mutations to workflows.
"""

from __future__ import annotations

from typing import Any, Final

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationDetailSerializer,
    PatientRegistrationUpdateSerializer,
)
from apps.patient_management.registration.models import PatientRegistration
from apps.patient_management.registration.permissions import (
    CanDeleteRegistration,
    CanUpdateRegistration,
    CanViewRegistration,
)
from apps.patient_management.registration.selectors import (
    get_registration_by_uuid,
)
from apps.patient_management.registration.workflows import (
    RegistrationDeletionRequest,
    RegistrationDeletionWorkflow,
    RegistrationUpdateRequest,
    RegistrationUpdateWorkflow,
)
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

REGISTRATION_TAG: Final[tuple[str, ...]] = ("Patient Registrations",)


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient registration.

    GET:
        Organization-scoped selector.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "registration_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewRegistration,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateRegistration,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateRegistration,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteRegistration,
        ),
    }

    serializer_classes = {
        "GET": PatientRegistrationDetailSerializer,
        "PUT": PatientRegistrationUpdateSerializer,
        "PATCH": PatientRegistrationUpdateSerializer,
    }

    detail_serializer_class = PatientRegistrationDetailSerializer

    update_workflow = RegistrationUpdateWorkflow
    delete_workflow = RegistrationDeletionWorkflow

    update_success_message = "Patient registration updated successfully."

    delete_success_message = "Patient registration deleted successfully."

    def _resolve_organization(self):
        """
        Resolve the organization from the authenticated request context.

        Organization is never accepted as client-controlled input.
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

        return organization

    def get_object(self) -> PatientRegistration:
        """
        Resolve the registration through the organization-scoped selector.
        """

        organization = self._resolve_organization()

        if organization is None:
            raise NotFound("Organization context is required.")

        return get_registration_by_uuid(
            uuid=self.kwargs[self.lookup_url_kwarg],
            organization=organization,
        )

    def build_update_workflow_request(
        self,
        instance: PatientRegistration,
        validated_data: dict[str, Any],
    ) -> RegistrationUpdateRequest:
        """
        Build the organization-scoped registration update request.
        """

        organization = self._resolve_organization()

        if organization is None:
            raise NotFound("Organization context is required.")

        return RegistrationUpdateRequest(
            organization_id=organization.pk,
            registration_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: PatientRegistration,
    ) -> RegistrationDeletionRequest:
        """
        Build the organization-scoped registration deletion request.
        """

        organization = self._resolve_organization()

        if organization is None:
            raise NotFound("Organization context is required.")

        return RegistrationDeletionRequest(
            organization_id=organization.pk,
            registration_id=instance.id,
        )


__all__ = ("PatientRegistrationRetrieveUpdateDestroyAPIView",)
