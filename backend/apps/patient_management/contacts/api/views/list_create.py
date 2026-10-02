"""
Patient Contact list/create API.

GET:
    API → Permission → Selector → Organization-scoped QuerySet

POST:
    API → Serializer → Workflow → Policy → Service → Domain Event
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.patient_management.contacts.api.filters import (
    ContactFilter,
)
from apps.patient_management.contacts.api.serializers import (
    ContactCreateSerializer,
    ContactDetailSerializer,
    ContactListSerializer,
)
from apps.patient_management.contacts.permissions import (
    CanCreateContact,
    CanViewContact,
)
from apps.patient_management.contacts.selectors import (
    ContactSelector,
)
from apps.patient_management.contacts.workflows import (
    ContactCreationRequest,
    ContactCreationWorkflow,
)
from apps.platform.organizations.models import Organization

CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Contacts",)


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create patient contacts.
    """

    filterset_class = ContactFilter

    search_fields = ("value",)

    ordering_fields = (
        "created_at",
        "updated_at",
        "contact_type",
        "purpose",
        "status",
        "is_primary",
        "is_preferred",
    )

    ordering = (
        "-is_primary",
        "contact_type",
    )

    lookup_url_kwarg = "contact_id"

    list_serializer_class = ContactListSerializer
    detail_serializer_class = ContactDetailSerializer
    create_serializer_class = ContactCreateSerializer

    create_workflow = ContactCreationWorkflow

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewContact,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateContact,
        ),
    }

    def get_queryset(self):
        """
        Return contacts restricted to the current organization.
        """
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return ContactSelector.queryset(
            organization=organization,
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> ContactCreationRequest:
        """
        Build the Contact creation workflow request.

        The organization is always taken from server-side context.
        It is never trusted from request payload data.
        """
        organization = self.current_organization

        if not isinstance(
            organization,
            Organization,
        ):
            raise RuntimeError(
                "Organization context is required.",
            )

        data = dict(validated_data)

        patient_id = data.pop(
            "patient_id",
            None,
        )

        if patient_id is None:
            raise ValueError(
                "Patient is required.",
            )

        return ContactCreationRequest(
            organization_id=organization.id,
            patient_id=patient_id,
            data=data,
        )

    def resolve_workflow_created_instance(
        self,
        result,
    ):
        """
        Resolve the created Contact model instance.

        The shared workflow mixin supports DTO-based workflow results,
        while serializers require the actual model instance.
        """
        data = result.data

        if data is None:
            return None

        contact_id = getattr(
            data,
            "contact_id",
            None,
        )

        if contact_id is None:
            return None

        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        return ContactSelector.get(
            organization=organization,
            contact_id=contact_id,
        )


__all__ = ("ContactListCreateAPIView",)
