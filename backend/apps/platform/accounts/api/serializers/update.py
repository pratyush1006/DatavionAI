"""
Update serializer for the Accounts application.
"""

from __future__ import annotations

from apps.platform.accounts.models import User
from apps.platform.accounts.services import UserService

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

    def update(
        self,
        instance: User,
        validated_data: dict,
    ) -> User:
        """
        Update a user.
        """

        return UserService.update(
            user=instance,
            **validated_data,
        )


__all__ = [
    "UserUpdateSerializer",
]
