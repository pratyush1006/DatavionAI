"""
List serializer for the Accounts application.
"""

from __future__ import annotations

from apps.platform.accounts.models import User

from .base import UserBaseSerializer
from .fields import LIST_FIELDS


class UserListSerializer(UserBaseSerializer):
    """
    Serializer for listing users.
    """

    class Meta(UserBaseSerializer.Meta):
        model = User
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS


__all__ = [
    "UserListSerializer",
]
