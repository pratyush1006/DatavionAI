"""
Base serializer for PermissionGroup.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    PermissionGroup,
)
from rest_framework import serializers


class PermissionGroupBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for PermissionGroup.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = PermissionGroup

        fields = (
            "id",
            "name",
            "code",
            "module",
            "description",
            "permissions",
            "display_order",
            "is_system",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "code",
            "created_at",
            "updated_at",
        )


__all__ = [
    "PermissionGroupBaseSerializer",
]
