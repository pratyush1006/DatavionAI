"""
Current user serializer.
"""

from __future__ import annotations

from apps.platform.accounts.models import User

from ..base import UserBaseSerializer


class MeSerializer(UserBaseSerializer):
    """
    Serializer for the authenticated user.
    """

    class Meta(UserBaseSerializer.Meta):
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_verified",
            "organization",
        )

        read_only_fields = fields


__all__ = [
    "MeSerializer",
]
