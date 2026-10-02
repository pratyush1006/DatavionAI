"""
API views for retrieving, updating, and deleting Patient Relationships.

Architecture
------------
GET
    Selector-driven.

PUT/PATCH
    Workflow-driven.

DELETE
    Workflow-driven.
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.relationships.api.serializers import (
    PatientRelationshipDetailSerializer,
    PatientRelationshipUpdateSerializer,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)
from apps.patient_management.relationships.selectors import (
    PatientRelationshipSelector,
)
from apps.patient_management.relationships.workflows import (
    PatientRelationshipDeletionRequest,
    PatientRelationshipDeletionWorkflow,
    PatientRelationshipUpdateRequest,
    PatientRelationshipUpdateWorkflow,
)

RELATIONSHIP_TAG: Final[tuple[str, ...]] = ("Patient Relationships",)


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a Patient Relationship.
    """

    lookup_url_kwarg = "relationship_id"

    permission_classes_map = {
        "GET": (IsAuthenticated,),
        "PUT": (IsAuthenticated,),
        "PATCH": (IsAuthenticated,),
        "DELETE": (IsAuthenticated,),
    }

    serializer_classes = {
        "GET": PatientRelationshipDetailSerializer,
        "PUT": PatientRelationshipUpdateSerializer,
        "PATCH": PatientRelationshipUpdateSerializer,
    }

    detail_serializer_class = PatientRelationshipDetailSerializer

    update_workflow = PatientRelationshipUpdateWorkflow

    delete_workflow = PatientRelationshipDeletionWorkflow

    update_success_message = "Patient relationship updated successfully."

    delete_success_message = "Patient relationship deleted successfully."

    def _get_organization(self):
        """
        Resolve the trusted organization context.
        """
        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            organization_roles = getattr(
                self.request.user,
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
            raise NotFound(
                "Organization context is required.",
            )

        return organization

    def get_object(
        self,
    ) -> PatientRelationship:
        """
        Resolve the relationship through the organization-scoped selector.
        """
        organization = self._get_organization()

        try:
            return PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self.kwargs[self.lookup_url_kwarg],
            )
        except PatientRelationship.DoesNotExist as exc:
            raise NotFound(
                "Patient relationship was not found.",
            ) from exc

    def build_update_workflow_request(
        self,
        instance: PatientRelationship,
        validated_data: dict[str, Any],
    ) -> PatientRelationshipUpdateRequest:
        """
        Build the update workflow request.
        """
        return PatientRelationshipUpdateRequest(
            relationship_id=instance.pk,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: PatientRelationship,
    ) -> PatientRelationshipDeletionRequest:
        """
        Build the deletion workflow request.
        """
        return PatientRelationshipDeletionRequest(
            relationship_id=instance.pk,
        )


__all__ = ("PatientRelationshipRetrieveUpdateDestroyAPIView",)
