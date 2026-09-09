"""
Patient Contact retrieve/update/delete API.

Architecture:

GET
    API → Permission → Selector

PUT/PATCH
    API → Serializer → Workflow → Policy → Service → Domain Event

DELETE
    API → Workflow → Policy → Service → Domain Event
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.contacts.api.serializers import (
    ContactDetailSerializer,
    ContactUpdateSerializer,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.permissions import (
    CanDeleteContact,
    CanUpdateContact,
    CanViewContact,
)
from apps.patient_management.contacts.selectors import (
    ContactSelector,
)
from apps.patient_management.contacts.workflows import (
    ContactDeletionRequest,
    ContactDeletionWorkflow,
    ContactUpdateRequest,
    ContactUpdateWorkflow,
)

CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Contacts",)


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient contact.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "contact_id"

    serializer_classes = {
        "GET": ContactDetailSerializer,
        "PUT": ContactUpdateSerializer,
        "PATCH": ContactUpdateSerializer,
    }

    detail_serializer_class = ContactDetailSerializer

    update_workflow = ContactUpdateWorkflow
    delete_workflow = ContactDeletionWorkflow

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewContact,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateContact,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateContact,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteContact,
        ),
    }

    update_success_message = "Patient contact updated successfully."

    delete_success_message = "Patient contact deleted successfully."

    def get_queryset(self):
        """
        Return only contacts belonging to the current organization.
        """
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return ContactSelector.queryset(
            organization=organization,
        )

    def get_object(self) -> Contact:
        """
        Resolve the Contact through the organization-scoped selector.

        Object-level permission is explicitly checked after selector
        resolution, matching the common DatavionOS base-view contract.
        """
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        contact = ContactSelector.get(
            organization=organization,
            contact_id=self.kwargs[self.lookup_url_kwarg],
        )

        self.check_object_permissions(
            contact,
        )

        return contact

    def build_update_workflow_request(
        self,
        instance: Contact,
        validated_data: dict[str, Any],
    ) -> ContactUpdateRequest:
        """
        Build the Contact update workflow request.
        """
        return ContactUpdateRequest(
            contact_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: Contact,
    ) -> ContactDeletionRequest:
        """
        Build the Contact deletion workflow request.
        """
        return ContactDeletionRequest(
            contact_id=instance.id,
        )


__all__ = ("ContactRetrieveUpdateDestroyAPIView",)
