"""
Role permission detail serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    RolePermission,
)


class RolePermissionDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for role permission details.
    """

    role_name = serializers.CharField(
        source="role.name",
        read_only=True,
    )

    role_code = serializers.CharField(
        source="role.code",
        read_only=True,
    )

    permission_name = serializers.CharField(
        source="permission.name",
        read_only=True,
    )

    permission_code = serializers.CharField(
        source="permission.code",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = RolePermission

        fields = (
            "id",
            "role",
            "role_name",
            "role_code",
            "permission",
            "permission_name",
            "permission_code",
            "assignment_type",
            "assignment_source",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = [
    "RolePermissionDetailSerializer",
]
