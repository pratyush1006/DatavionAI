"""
List and create API views for patient family members.
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.patient_management.family_members.api.filters import FamilyMemberFilter
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberCreateSerializer,
    FamilyMemberDetailSerializer,
    FamilyMemberListSerializer,
)
from apps.patient_management.family_members.permissions import (
    CanCreateFamilyMember,
    CanViewFamilyMember,
)
from apps.patient_management.family_members.selectors import FamilyMemberSelector
from apps.patient_management.family_members.workflows import (
    FamilyMemberCreationRequest,
    FamilyMemberCreationWorkflow,
)

FAMILY_MEMBER_TAG: Final = ("Patient Family Members",)


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberListCreateAPIView(BaseListCreateAPIView):
    """List and create patient family members."""

    filterset_class = FamilyMemberFilter

    search_fields = (
        "family_member_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "email",
        "relationship",
    )

    ordering_fields = (
        "created_at",
        "updated_at",
        "first_name",
        "last_name",
        "relationship",
        "status",
        "is_next_of_kin",
        "is_emergency_contact",
    )

    ordering = ("first_name", "last_name")
    lookup_url_kwarg = "family_member_id"

    list_serializer_class = FamilyMemberListSerializer
    detail_serializer_class = FamilyMemberDetailSerializer
    create_serializer_class = FamilyMemberCreateSerializer
    create_workflow = FamilyMemberCreationWorkflow

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewFamilyMember),
        "POST": (IsAuthenticated, CanCreateFamilyMember),
    }

    def get_queryset(self):
        organization = self.current_organization

        if organization is None:
            raise RuntimeError("Organization context is required.")

        return FamilyMemberSelector.queryset(
            organization=organization,
        )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> FamilyMemberCreationRequest:
        organization = self.current_organization

        if organization is None:
            raise RuntimeError("Organization context is required.")

        data = dict(validated_data)
        patient_id = data.pop("patient_id", None)

        if patient_id is None:
            raise ValueError("Patient is required.")

        return FamilyMemberCreationRequest(
            organization_id=organization.id,
            patient_id=patient_id,
            data=data,
        )

    def resolve_workflow_created_instance(self, result):
        if result.data is None:
            return None

        organization = self.current_organization

        if organization is None:
            raise RuntimeError("Organization context is required.")

        return FamilyMemberSelector.get(
            organization=organization,
            family_member_id=result.data.family_member_id,
        )


__all__ = ("FamilyMemberListCreateAPIView",)
