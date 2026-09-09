"""
Retrieve, update, and delete API views for patient family members.
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseRetrieveUpdateDestroyAPIView
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberDetailSerializer,
    FamilyMemberUpdateSerializer,
)
from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.family_members.permissions import (
    CanDeleteFamilyMember,
    CanUpdateFamilyMember,
    CanViewFamilyMember,
)
from apps.patient_management.family_members.selectors import FamilyMemberSelector
from apps.patient_management.family_members.workflows import (
    FamilyMemberDeletionRequest,
    FamilyMemberDeletionWorkflow,
    FamilyMemberUpdateRequest,
    FamilyMemberUpdateWorkflow,
)

FAMILY_MEMBER_TAG: Final = ("Patient Family Members",)


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """Retrieve, update, or soft-delete a patient family member."""

    lookup_url_kwarg = "family_member_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewFamilyMember),
        "PUT": (IsAuthenticated, CanUpdateFamilyMember),
        "PATCH": (IsAuthenticated, CanUpdateFamilyMember),
        "DELETE": (IsAuthenticated, CanDeleteFamilyMember),
    }

    serializer_classes = {
        "GET": FamilyMemberDetailSerializer,
        "PUT": FamilyMemberUpdateSerializer,
        "PATCH": FamilyMemberUpdateSerializer,
    }

    detail_serializer_class = FamilyMemberDetailSerializer
    update_workflow = FamilyMemberUpdateWorkflow
    delete_workflow = FamilyMemberDeletionWorkflow

    update_success_message = "Patient family member updated successfully."
    delete_success_message = "Patient family member deleted successfully."

    def _organization(self):
        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None and self.request.user.is_authenticated:
            role = self.request.user.organization_roles.select_related(
                "organization"
            ).first()
            organization = role.organization if role else None

        return organization

    def get_queryset(self):
        organization = self._organization()

        if organization is None:
            return FamilyMemberSelector.empty_queryset()

        return FamilyMemberSelector.queryset(
            organization=organization,
        )

    def get_object(self) -> FamilyMember:
        organization = self._organization()

        if organization is None:
            raise NotFound("Organization context is required.")

        member = FamilyMemberSelector.get(
            organization=organization,
            family_member_id=self.kwargs[self.lookup_url_kwarg],
        )

        self.check_object_permissions(
            self.request,
            member,
        )

        return member

    def build_update_workflow_request(
        self,
        instance: FamilyMember,
        validated_data: dict[str, Any],
    ) -> FamilyMemberUpdateRequest:
        return FamilyMemberUpdateRequest(
            family_member_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance: FamilyMember,
    ) -> FamilyMemberDeletionRequest:
        return FamilyMemberDeletionRequest(
            family_member_id=instance.id,
        )


__all__ = ("FamilyMemberRetrieveUpdateDestroyAPIView",)
