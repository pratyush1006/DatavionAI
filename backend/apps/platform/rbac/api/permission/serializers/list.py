"""
Permission list serializer.
"""

from __future__ import annotations

from .base import (
    PermissionBaseSerializer,
)


class PermissionListSerializer(
    PermissionBaseSerializer,
):
    """
    Serializer used for listing permissions.
    """


__all__ = [
    "PermissionListSerializer",
]
