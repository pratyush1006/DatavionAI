"""
List API view for Family Members.
"""

from __future__ import annotations

from apps.common.api import BaseListAPIView
from apps.patient_management.family_members.api.filters import (
    FamilyMemberFilter,
)
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberListSerializer,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)

__all__ = [
    "FamilyMemberListAPIView",
]


class FamilyMemberListAPIView(
    BaseListAPIView,
):
    """
    List family members.
    """

    queryset = FamilyMember.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = FamilyMemberListSerializer

    filterset_class = FamilyMemberFilter

    permission_required = (FamilyMemberPermission.LIST,)

    search_fields = (
        "family_member_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "email",
    )

    ordering_fields = (
        "created_at",
        "updated_at",
        "first_name",
        "relationship",
    )

    ordering = ("first_name",)
