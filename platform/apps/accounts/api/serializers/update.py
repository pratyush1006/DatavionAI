"""
Update serializer for the Accounts application.
"""

from __future__ import annotations

from .base import UserBaseSerializer
from .fields import UPDATE_FIELDS


class UserUpdateSerializer(UserBaseSerializer):
    """
    Serializer for updating users.
    """

    class Meta(UserBaseSerializer.Meta):
        fields = UPDATE_FIELDS

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
            },
        }


__all__ = [
    "UserUpdateSerializer",
]
