"""
Detail serializer for the Accounts application.
"""

from __future__ import annotations

from apps.platform.accounts.models import User

from .base import UserBaseSerializer
from .fields import DETAIL_FIELDS


class UserDetailSerializer(
    UserBaseSerializer,
):
    """
    Serializer for retrieving detailed user information.
    """

    class Meta(
        UserBaseSerializer.Meta,
    ):
        model = User

        fields = DETAIL_FIELDS

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "is_verified",
        )


__all__ = ("UserDetailSerializer",)
