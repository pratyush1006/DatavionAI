"""
Delete API view for Family Members.
"""

from __future__ import annotations

from rest_framework import status

from apps.common.api import BaseDestroyAPIView
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)

__all__ = [
    "FamilyMemberDeleteAPIView",
]


class FamilyMemberDeleteAPIView(
    BaseDestroyAPIView,
):
    """
    Soft delete a family member.
    """

    queryset = FamilyMember.objects.select_related(
        "organization",
        "patient",
    )

    permission_required = (FamilyMemberPermission.DELETE,)

    lookup_field = "id"

    success_status_code = status.HTTP_204_NO_CONTENT
