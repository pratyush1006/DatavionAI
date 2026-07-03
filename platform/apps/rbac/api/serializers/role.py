"""
Role serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import Role

ROLE_WRITE_FIELDS = (
    "name",
    "code",
    "description",
    "is_active",
)


class RoleListSerializer(RBACSerializer):
    """
    Serializer for listing roles.
    """

    class Meta:
        model = Role
        fields = (
            "id",
            *ROLE_WRITE_FIELDS,
        )
        read_only_fields = ("id",)


class RoleDetailSerializer(RoleListSerializer):
    """
    Serializer for retrieving role details.
    """

    class Meta(RoleListSerializer.Meta):
        fields = (
            *RoleListSerializer.Meta.fields,
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            *RoleListSerializer.Meta.read_only_fields,
            "created_at",
            "updated_at",
        )


class RoleCreateSerializer(RBACSerializer):
    """
    Serializer for creating roles.
    """

    class Meta:
        model = Role
        fields = ROLE_WRITE_FIELDS


class RoleUpdateSerializer(RBACSerializer):
    """
    Serializer for updating roles.
    """

    class Meta:
        model = Role
        fields = ROLE_WRITE_FIELDS
