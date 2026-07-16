"""
Create serializer for the Accounts application.
"""

from __future__ import annotations

from apps.platform.accounts.services import UserService

from .base import UserBaseSerializer
from .fields import CREATE_FIELDS


class UserCreateSerializer(UserBaseSerializer):
    """
    Serializer for creating users.
    """

    class Meta(UserBaseSerializer.Meta):
        fields = CREATE_FIELDS

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(
        self,
        validated_data: dict,
    ):
        """
        Create a user.
        """

        return UserService.create(
            **validated_data,
        )


__all__ = [
    "UserCreateSerializer",
]
