"""
List serializer for PermissionGroup.
"""

from __future__ import annotations

from .base import (
    PermissionGroupBaseSerializer,
)


class PermissionGroupListSerializer(
    PermissionGroupBaseSerializer,
):
    """
    Serializer used for listing permission groups.
    """


__all__ = [
    "PermissionGroupListSerializer",
]
