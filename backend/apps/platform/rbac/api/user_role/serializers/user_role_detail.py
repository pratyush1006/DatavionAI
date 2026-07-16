"""
User role detail serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    UserRole,
)
from rest_framework import serializers


class UserRoleDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for user role details.
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
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = [
    "UserRoleDetailSerializer",
]
