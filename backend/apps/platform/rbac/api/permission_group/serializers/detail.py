"""
Detail serializer for PermissionGroup.
"""

from __future__ import annotations

from .base import (
    PermissionGroupBaseSerializer,
)


class PermissionGroupDetailSerializer(
    PermissionGroupBaseSerializer,
):
    """
    Serializer used for retrieving a permission group.
    """


__all__ = [
    "PermissionGroupDetailSerializer",
]
