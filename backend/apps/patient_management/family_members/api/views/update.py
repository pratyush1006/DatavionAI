"""
Update API view for Family Members.
"""

from __future__ import annotations

from apps.common.api import BaseUpdateAPIView
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberUpdateSerializer,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)

__all__ = [
    "FamilyMemberUpdateAPIView",
]


class FamilyMemberUpdateAPIView(
    BaseUpdateAPIView,
):
    """
    Update a family member.
    """

    queryset = FamilyMember.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = FamilyMemberUpdateSerializer

    permission_required = (FamilyMemberPermission.UPDATE,)

    lookup_field = "id"
