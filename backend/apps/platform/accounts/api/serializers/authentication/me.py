"""
Current user serializer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import UserBaseSerializer

if TYPE_CHECKING:
    pass


class MeSerializer(
    UserBaseSerializer,
):
    """
    Serializer for authenticated user.
    """

    class Meta(
        UserBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_verified",
        )

        read_only_fields = fields


__all__ = ("MeSerializer",)
