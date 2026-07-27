"""
Detail API view for Family Members.
"""

from __future__ import annotations

from apps.common.api import BaseRetrieveAPIView
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberDetailSerializer,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)

__all__ = [
    "FamilyMemberDetailAPIView",
]


class FamilyMemberDetailAPIView(
    BaseRetrieveAPIView,
):
    """
    Retrieve a family member.
    """

    queryset = FamilyMember.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = FamilyMemberDetailSerializer

    permission_required = (FamilyMemberPermission.VIEW,)

    lookup_field = "id"
