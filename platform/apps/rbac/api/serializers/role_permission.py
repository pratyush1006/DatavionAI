"""
Role-permission assignment serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import RolePermission

ROLE_PERMISSION_WRITE_FIELDS = (
    "role",
    "permission",
)


class RolePermissionListSerializer(RBACSerializer):
    """
    Serializer for listing role-permission assignments.
    """

    class Meta:
        model = RolePermission
        fields = (
            "id",
            "role",
            "permission",
        )
        read_only_fields = ("id",)


class RolePermissionDetailSerializer(RolePermissionListSerializer):
    """
    Serializer for retrieving a role-permission assignment.
    """

    class Meta(RolePermissionListSerializer.Meta):
        fields = (
            *RolePermissionListSerializer.Meta.fields,
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            *RolePermissionListSerializer.Meta.read_only_fields,
            "created_at",
            "updated_at",
        )


class RolePermissionCreateSerializer(RBACSerializer):
    """
    Serializer for assigning a permission to a role.
    """

    class Meta:
        model = RolePermission
        fields = ROLE_PERMISSION_WRITE_FIELDS
