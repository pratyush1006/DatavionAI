"""
Permission update serializer.
"""

from __future__ import annotations

from .base import (
    PermissionBaseSerializer,
)


class PermissionUpdateSerializer(
    PermissionBaseSerializer,
):
    """
    Serializer used for updating permissions.
    """

    class Meta(
        PermissionBaseSerializer.Meta,
    ):
        read_only_fields = (
            "id",
            "code",
        )


__all__ = [
    "PermissionUpdateSerializer",
]
