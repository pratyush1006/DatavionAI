"""
Permission create serializer.
"""

from __future__ import annotations

from .base import (
    PermissionBaseSerializer,
)


class PermissionCreateSerializer(
    PermissionBaseSerializer,
):
    """
    Serializer used for creating permissions.
    """

    class Meta(
        PermissionBaseSerializer.Meta,
    ):
        read_only_fields = (
            "id",
            "code",
        )


__all__ = [
    "PermissionCreateSerializer",
]
