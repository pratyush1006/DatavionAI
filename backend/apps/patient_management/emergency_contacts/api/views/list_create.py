"""
Patient Emergency Contact list/create API.

GET:
    API → Permission → Selector → Organization-scoped QuerySet

POST:
    API → Serializer → Workflow → Policy → Service → Domain Event
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.patient_management.emergency_contacts.api.filters import (
    EmergencyContactFilter,
)
from apps.patient_management.emergency_contacts.api.serializers import (
    EmergencyContactCreateSerializer,
    EmergencyContactDetailSerializer,
    EmergencyContactListSerializer,
)
from apps.patient_management.emergency_contacts.permissions import (
    CanCreateEmergencyContact,
    CanViewEmergencyContact,
)
from apps.patient_management.emergency_contacts.selectors import (
    EmergencyContactSelector,
)
from apps.patient_management.emergency_contacts.workflows import (
    EmergencyContactCreationRequest,
    EmergencyContactCreationWorkflow,
)
from apps.platform.organizations.models import Organization

EMERGENCY_CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Emergency Contacts",)


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create patient emergency contacts.
    """

    filterset_class = EmergencyContactFilter

    search_fields = (
        "emergency_contact_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "alternate_mobile_number",
        "home_phone",
        "work_phone",
        "email",
    )

    ordering_fields = (
        "created_at",
        "updated_at",
        "first_name",
        "last_name",
        "relationship",
        "priority_order",
        "status",
        "is_primary",
        "is_verified",
    )

    ordering = (
        "-is_primary",
        "priority_order",
        "first_name",
        "last_name",
    )

    lookup_url_kwarg = "emergency_contact_id"

    list_serializer_class = EmergencyContactListSerializer
    detail_serializer_class = EmergencyContactDetailSerializer
    create_serializer_class = EmergencyContactCreateSerializer

    create_workflow = EmergencyContactCreationWorkflow

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewEmergencyContact,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateEmergencyContact,
        ),
    }

    def get_queryset(self):
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return EmergencyContactSelector.queryset(
            organization=organization,
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> EmergencyContactCreationRequest:
        organization = self.current_organization

        if not isinstance(
            organization,
            Organization,
        ):
            raise RuntimeError(
                "Organization context is required.",
            )

        data = dict(
            validated_data,
        )

        patient_id = data.pop(
            "patient_id",
            None,
        )

        if patient_id is None:
            raise ValueError(
                "Patient is required.",
            )

        return EmergencyContactCreationRequest(
            organization_id=organization.id,
            patient_id=patient_id,
            data=data,
        )

    def resolve_workflow_created_instance(
        self,
        result,
    ):
        data = result.data

        if data is None:
            return None

        emergency_contact_id = getattr(
            data,
            "emergency_contact_id",
            None,
        )

        if emergency_contact_id is None:
            return None

        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return EmergencyContactSelector.get(
            organization=organization,
            emergency_contact_id=emergency_contact_id,
        )


__all__ = ("EmergencyContactListCreateAPIView",)
