"""
Create API view for Family Members.
"""

from __future__ import annotations

from rest_framework import status

from apps.common.api import BaseCreateAPIView
from apps.patient_management.family_members.api.serializers import (
    FamilyMemberCreateSerializer,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)

__all__ = [
    "FamilyMemberCreateAPIView",
]


class FamilyMemberCreateAPIView(
    BaseCreateAPIView,
):
    """
    Create a family member.
    """

    queryset = FamilyMember.objects.all()

    serializer_class = FamilyMemberCreateSerializer

    permission_required = (FamilyMemberPermission.CREATE,)

    success_status_code = status.HTTP_201_CREATED
