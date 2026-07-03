"""
Permission serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import Permission

PERMISSION_WRITE_FIELDS = (
    "name",
    "code",
    "description",
    "is_active",
)


class PermissionListSerializer(RBACSerializer):
    """
    Serializer for listing permissions.
    """

    class Meta:
        model = Permission
        fields = (
            "id",
            *PERMISSION_WRITE_FIELDS,
        )
        read_only_fields = ("id",)


class PermissionDetailSerializer(PermissionListSerializer):
    """
    Serializer for retrieving permission details.
    """

    class Meta(PermissionListSerializer.Meta):
        fields = (
            *PermissionListSerializer.Meta.fields,
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            *PermissionListSerializer.Meta.read_only_fields,
            "created_at",
            "updated_at",
        )


class PermissionCreateSerializer(RBACSerializer):
    """
    Serializer for creating permissions.
    """

    class Meta:
        model = Permission
        fields = PERMISSION_WRITE_FIELDS


class PermissionUpdateSerializer(RBACSerializer):
    """
    Serializer for updating permissions.
    """

    class Meta:
        model = Permission
        fields = PERMISSION_WRITE_FIELDS
