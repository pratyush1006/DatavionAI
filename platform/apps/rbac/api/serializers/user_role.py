"""
User-role assignment serializers.
"""

from __future__ import annotations

from apps.rbac.api.serializers.base import RBACSerializer
from apps.rbac.models import UserRole

USER_ROLE_WRITE_FIELDS = (
    "user",
    "role",
)


class UserRoleListSerializer(RBACSerializer):
    """
    Serializer for listing user-role assignments.
    """

    class Meta:
        model = UserRole
        fields = (
            "id",
            "user",
            "role",
        )
        read_only_fields = ("id",)


class UserRoleDetailSerializer(UserRoleListSerializer):
    """
    Serializer for retrieving a user-role assignment.
    """

    class Meta(UserRoleListSerializer.Meta):
        fields = (
            *UserRoleListSerializer.Meta.fields,
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            *UserRoleListSerializer.Meta.read_only_fields,
            "created_at",
            "updated_at",
        )


class UserRoleCreateSerializer(RBACSerializer):
    """
    Serializer for assigning a role to a user.
    """

    class Meta:
        model = UserRole
        fields = USER_ROLE_WRITE_FIELDS


class UserRoleUpdateSerializer(RBACSerializer):
    """
    Updating user-role assignments is not supported.
    """

    class Meta:
        model = UserRole
        fields = USER_ROLE_WRITE_FIELDS

    def validate(self, attrs):
        raise NotImplementedError(
            "User-role assignments cannot be updated. "
            "Delete the assignment and create a new one instead."
        )
