"""
User role create serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.services import (
    create_user_role,
)
from rest_framework import serializers


class UserRoleCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating user role assignments.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = UserRole

        fields = (
            "id",
            "user",
            "role",
            "assignment_source",
            "is_active",
        )

        read_only_fields = ("id",)

    def create(
        self,
        validated_data,
    ) -> UserRole:
        """
        Create a user role assignment.
        """

        return create_user_role(
            validated_data=validated_data,
        )


__all__ = [
    "UserRoleCreateSerializer",
]
