"""
API views for retrieving, updating, and deleting patient identifiers.

Architecture:

GET
    Selector driven

PUT/PATCH
    Workflow driven

DELETE
    Workflow driven
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.identifiers.api.serializers import (
    PatientIdentifierDetailSerializer,
    PatientIdentifierUpdateSerializer,
)
from apps.patient_management.identifiers.permissions import (
    CanDeleteIdentifier,
    CanUpdateIdentifier,
    CanViewIdentifier,
)
from apps.patient_management.identifiers.selectors import (
    get_identifier_by_id,
)
from apps.patient_management.identifiers.workflows import (
    IdentifierDeletionRequest,
    IdentifierDeletionWorkflow,
    IdentifierUpdateRequest,
    IdentifierUpdateWorkflow,
)

IDENTIFIER_TAG: Final[tuple[str, ...]] = ("Patient Identifiers",)


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient identifier.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "identifier_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewIdentifier,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateIdentifier,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateIdentifier,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteIdentifier,
        ),
    }

    serializer_classes = {
        "GET": PatientIdentifierDetailSerializer,
        "PUT": PatientIdentifierUpdateSerializer,
        "PATCH": PatientIdentifierUpdateSerializer,
    }

    detail_serializer_class = PatientIdentifierDetailSerializer

    update_workflow = IdentifierUpdateWorkflow

    delete_workflow = IdentifierDeletionWorkflow

    update_success_message = "Patient identifier updated successfully."

    delete_success_message = "Patient identifier deleted successfully."

    def get_object(self):
        """
        Resolve the identifier through the organization-scoped selector.
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
            from rest_framework.exceptions import NotFound

            raise NotFound("Organization context is required.")

        return get_identifier_by_id(
            identifier_id=self.kwargs[self.lookup_url_kwarg],
            organization=organization,
        )

    def build_update_workflow_request(
        self,
        instance,
        validated_data: dict[str, Any],
    ) -> IdentifierUpdateRequest:
        """
        Build the Patient Identifier update workflow request.
        """
        return IdentifierUpdateRequest(
            identifier_id=instance.pk,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> IdentifierDeletionRequest:
        """
        Build the Patient Identifier deletion workflow request.
        """
        return IdentifierDeletionRequest(
            identifier_id=instance.pk,
        )


__all__ = ("PatientIdentifierRetrieveUpdateDestroyAPIView",)
