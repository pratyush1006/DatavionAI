"""
User role update serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.services import (
    update_user_role,
)


class UserRoleUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating user role assignments.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = UserRole

        fields = (
            "user",
            "role",
            "assignment_source",
            "is_active",
        )

    def update(
        self,
        instance: UserRole,
        validated_data,
    ) -> UserRole:
        """
        Update a user role assignment.
        """

        return update_user_role(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "UserRoleUpdateSerializer",
]
