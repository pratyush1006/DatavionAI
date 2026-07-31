"""
User role list serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    UserRole,
)


class UserRoleListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing user role assignments.
    """

    user_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    role_name = serializers.CharField(
        source="role.name",
        read_only=True,
    )

    role_code = serializers.CharField(
        source="role.code",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = UserRole

        fields = (
            "id",
            "user",
            "user_name",
            "user_email",
            "role",
            "role_name",
            "role_code",
            "assignment_source",
            "is_active",
        )

        read_only_fields = fields


__all__ = [
    "UserRoleListSerializer",
]
