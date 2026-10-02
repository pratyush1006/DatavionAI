"""
Role permission update serializer.
"""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

from apps.platform.rbac.constants import (
    RolePermissionSource,
    RolePermissionType,
)
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.services import (
    update_role_permission,
)


class RolePermissionUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating a role permission.
    """

    assignment_type = serializers.ChoiceField(
        choices=RolePermissionType.choices,
        required=False,
    )

    assignment_source = serializers.ChoiceField(
        choices=RolePermissionSource.choices,
        required=False,
    )

    class Meta:
        model = RolePermission

        fields = (
            "role",
            "permission",
            "assignment_type",
            "assignment_source",
            "is_active",
        )

    def update(
        self,
        instance: RolePermission,
        validated_data: dict[str, Any],
    ) -> RolePermission:
        """
        Update role permission.
        """

        return update_role_permission(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "RolePermissionUpdateSerializer",
]
