"""
Permission detail serializer.
"""

from __future__ import annotations

from .base import (
    PERMISSION_FIELDS,
    PermissionBaseSerializer,
)


class PermissionDetailSerializer(
    PermissionBaseSerializer,
):
    """
    Serializer for permission details.
    """

    class Meta(
        PermissionBaseSerializer.Meta,
    ):
        fields = (
            *PERMISSION_FIELDS,
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = [
    "PermissionDetailSerializer",
]
