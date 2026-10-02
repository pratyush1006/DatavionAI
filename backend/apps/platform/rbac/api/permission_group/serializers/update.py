"""
Update serializer for PermissionGroup.
"""

from __future__ import annotations

from .base import (
    PermissionGroupBaseSerializer,
)


class PermissionGroupUpdateSerializer(
    PermissionGroupBaseSerializer,
):
    """
    Serializer used for updating permission groups.
    """


__all__ = [
    "PermissionGroupUpdateSerializer",
]
