"""
Create serializer for PermissionGroup.
"""

from __future__ import annotations

from .base import (
    PermissionGroupBaseSerializer,
)


class PermissionGroupCreateSerializer(
    PermissionGroupBaseSerializer,
):
    """
    Serializer used for creating permission groups.
    """


__all__ = [
    "PermissionGroupCreateSerializer",
]
