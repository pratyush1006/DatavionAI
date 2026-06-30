"""
Role serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import Role


class RoleListSerializer(RBACSerializer):
    """
    Serializer for listing roles.
    """

    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "code",
            "description",
            "is_active",
        )


class RoleDetailSerializer(RoleListSerializer):
    """
    Serializer for role details.
    """

    class Meta(RoleListSerializer.Meta):
        fields = (
            *RoleListSerializer.Meta.fields,
            "created_at",
            "updated_at",
        )


class RoleCreateSerializer(RBACSerializer):
    """
    Serializer for creating roles.
    """

    class Meta:
        model = Role
        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )


class RoleUpdateSerializer(RBACSerializer):
    """
    Serializer for updating roles.
    """

    class Meta:
        model = Role
        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )
