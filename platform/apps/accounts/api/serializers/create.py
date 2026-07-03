"""
Create serializer for the Accounts application.
"""

from __future__ import annotations

from .base import UserBaseSerializer
from .fields import WRITE_FIELDS


class UserCreateSerializer(UserBaseSerializer):
    """
    Serializer for creating users.
    """

    class Meta(UserBaseSerializer.Meta):
        fields = WRITE_FIELDS

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }


__all__ = [
    "UserCreateSerializer",
]
