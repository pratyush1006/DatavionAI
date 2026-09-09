"""
Patient Emergency Contact retrieve/update/delete API.
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.emergency_contacts.api.serializers import (
    EmergencyContactDetailSerializer,
    EmergencyContactUpdateSerializer,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.permissions import (
    CanDeleteEmergencyContact,
    CanUpdateEmergencyContact,
    CanViewEmergencyContact,
)
from apps.patient_management.emergency_contacts.selectors import (
    EmergencyContactSelector,
)
from apps.patient_management.emergency_contacts.workflows import (
    EmergencyContactDeletionRequest,
    EmergencyContactDeletionWorkflow,
    EmergencyContactUpdateRequest,
    EmergencyContactUpdateWorkflow,
)

EMERGENCY_CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Emergency Contacts",)


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient emergency contact.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "emergency_contact_id"

    serializer_classes = {
        "GET": EmergencyContactDetailSerializer,
        "PUT": EmergencyContactUpdateSerializer,
        "PATCH": EmergencyContactUpdateSerializer,
    }

    detail_serializer_class = EmergencyContactDetailSerializer

    update_workflow = EmergencyContactUpdateWorkflow
    delete_workflow = EmergencyContactDeletionWorkflow

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEmergencyContact,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateEmergencyContact,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateEmergencyContact,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteEmergencyContact,
        ),
    }

    update_success_message = "Emergency contact updated successfully."

    delete_success_message = "Emergency contact deleted successfully."

    def get_queryset(self):
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return EmergencyContactSelector.queryset(
            organization=organization,
        )

    def get_object(self) -> EmergencyContact:
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        emergency_contact = EmergencyContactSelector.get(
            organization=organization,
            emergency_contact_id=self.kwargs[self.lookup_url_kwarg],
        )

        self.check_object_permissions(
            emergency_contact,
        )

        return emergency_contact

    def build_update_workflow_request(
        self,
        instance: EmergencyContact,
        validated_data: dict[str, Any],
    ) -> EmergencyContactUpdateRequest:
        return EmergencyContactUpdateRequest(
            emergency_contact_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: EmergencyContact,
    ) -> EmergencyContactDeletionRequest:
        return EmergencyContactDeletionRequest(
            emergency_contact_id=instance.id,
        )


__all__ = ("EmergencyContactRetrieveUpdateDestroyAPIView",)
