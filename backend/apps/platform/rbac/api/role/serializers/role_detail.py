"""
Role detail serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    Role,
)
from rest_framework import serializers


class RoleDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for retrieving a role.
    """

    parent = serializers.StringRelatedField(
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
            "description",
            "role_type",
            "scope",
            "category",
            "parent",
            "priority",
            "display_order",
            "is_system",
            "is_default",
            "is_assignable",
            "is_editable",
            "is_deletable",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = [
    "RoleDetailSerializer",
]
