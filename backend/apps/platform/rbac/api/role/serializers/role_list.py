"""
Role list serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    Role,
)
from rest_framework import serializers


class RoleListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing roles.
    """

    parent_name = serializers.CharField(
        source="parent.name",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = Role

        fields = (
            "id",
            "name",
            "code",
            "role_type",
            "scope",
            "category",
            "priority",
            "display_order",
            "parent_name",
            "is_system",
            "is_default",
            "is_assignable",
            "is_active",
        )

        read_only_fields = fields


__all__ = [
    "RoleListSerializer",
]
