"""
Lifecycle API views for Patient Family Members.
"""

from __future__ import annotations

from typing import Final
from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberDetailSerializer,
)
from apps.patient_management.family_members.permissions import (
    CanManageEmergencyContactFamilyMember,
    CanManageNextOfKinFamilyMember,
    CanRestoreFamilyMember,
    CanUpdateFamilyMember,
)
from apps.patient_management.family_members.selectors import FamilyMemberSelector
from apps.patient_management.family_members.workflows import (
    FamilyMemberActivationRequest,
    FamilyMemberActivationWorkflow,
    FamilyMemberDeactivationRequest,
    FamilyMemberDeactivationWorkflow,
    FamilyMemberEmergencyContactRequest,
    FamilyMemberEmergencyContactWorkflow,
    FamilyMemberNextOfKinRequest,
    FamilyMemberNextOfKinWorkflow,
    FamilyMemberRestoreRequest,
    FamilyMemberRestoreWorkflow,
)

FAMILY_MEMBER_TAG: Final = ("Patient Family Members",)


class FamilyMemberLifecycleAPIView(BaseGenericAPIView):
    """Common implementation for Family Member lifecycle operations."""

    def _organization(self):
        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            raise RuntimeError("Organization context is required.")

        return organization

    def _get_family_member(
        self,
        family_member_id: UUID,
        *,
        deleted: bool = False,
    ):
        organization = self._organization()

        member = (
            FamilyMemberSelector.get_deleted(
                organization=organization,
                family_member_id=family_member_id,
            )
            if deleted
            else FamilyMemberSelector.get(
                organization=organization,
                family_member_id=family_member_id,
            )
        )

        self.check_object_permissions(member)
        return member

    def _execute(
        self,
        *,
        member,
        workflow,
        request,
        message: str,
    ):
        result = workflow(
            request=request,
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message or "Family Member workflow execution failed.",
            )

        refreshed = self._get_family_member(member.id)

        return self.success_response(
            data=FamilyMemberDetailSerializer(
                refreshed,
                context={"request": self.request},
            ).data,
            message=result.message or message,
        )


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberActivateAPIView(FamilyMemberLifecycleAPIView):
    permission_classes_map = {
        "POST": (IsAuthenticated, CanUpdateFamilyMember),
    }

    def post(self, request, family_member_id: UUID, *args, **kwargs):
        member = self._get_family_member(family_member_id)

        return self._execute(
            member=member,
            workflow=FamilyMemberActivationWorkflow,
            request=FamilyMemberActivationRequest(
                family_member_id=member.id,
            ),
            message="Patient family member activated successfully.",
        )


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberDeactivateAPIView(FamilyMemberLifecycleAPIView):
    permission_classes_map = {
        "POST": (IsAuthenticated, CanUpdateFamilyMember),
    }

    def post(self, request, family_member_id: UUID, *args, **kwargs):
        member = self._get_family_member(family_member_id)

        return self._execute(
            member=member,
            workflow=FamilyMemberDeactivationWorkflow,
            request=FamilyMemberDeactivationRequest(
                family_member_id=member.id,
            ),
            message="Patient family member deactivated successfully.",
        )


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberRestoreAPIView(FamilyMemberLifecycleAPIView):
    permission_classes_map = {
        "POST": (IsAuthenticated, CanRestoreFamilyMember),
    }

    def post(self, request, family_member_id: UUID, *args, **kwargs):
        member = self._get_family_member(
            family_member_id,
            deleted=True,
        )

        return self._execute(
            member=member,
            workflow=FamilyMemberRestoreWorkflow,
            request=FamilyMemberRestoreRequest(
                family_member_id=member.id,
            ),
            message="Patient family member restored successfully.",
        )


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberSetNextOfKinAPIView(FamilyMemberLifecycleAPIView):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanManageNextOfKinFamilyMember,
        ),
    }

    def post(self, request, family_member_id: UUID, *args, **kwargs):
        member = self._get_family_member(family_member_id)

        return self._execute(
            member=member,
            workflow=FamilyMemberNextOfKinWorkflow,
            request=FamilyMemberNextOfKinRequest(
                family_member_id=member.id,
            ),
            message=("Patient family member set as next of kin successfully."),
        )


@extend_schema(tags=FAMILY_MEMBER_TAG)
class FamilyMemberSetEmergencyContactAPIView(
    FamilyMemberLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanManageEmergencyContactFamilyMember,
        ),
    }

    def post(self, request, family_member_id: UUID, *args, **kwargs):
        member = self._get_family_member(family_member_id)

        return self._execute(
            member=member,
            workflow=FamilyMemberEmergencyContactWorkflow,
            request=FamilyMemberEmergencyContactRequest(
                family_member_id=member.id,
            ),
            message=("Patient family member set as emergency contact successfully."),
        )


__all__ = (
    "FamilyMemberActivateAPIView",
    "FamilyMemberDeactivateAPIView",
    "FamilyMemberRestoreAPIView",
    "FamilyMemberSetEmergencyContactAPIView",
    "FamilyMemberSetNextOfKinAPIView",
)
