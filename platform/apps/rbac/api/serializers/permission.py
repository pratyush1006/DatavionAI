"""
Permission serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import Permission


class PermissionListSerializer(RBACSerializer):
    """
    Serializer for listing permissions.
    """

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "code",
            "description",
            "is_active",
        )


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


class PermissionCreateSerializer(RBACSerializer):
    """
    Serializer for creating permissions.
    """

    class Meta:
        model = Permission
        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )


class PermissionUpdateSerializer(RBACSerializer):
    """
    Serializer for updating permissions.
    """

    class Meta:
        model = Permission
        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )
