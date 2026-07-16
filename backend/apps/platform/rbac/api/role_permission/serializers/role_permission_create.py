"""
Role permission create serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.services import (
    create_role_permission,
)
from apps.platform.rbac.validators import (
    validate_role_permission,
)


class RolePermissionCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a role permission.
    """

    class Meta:
        model = RolePermission

        fields = (
            "role",
            "permission",
            "assignment_type",
            "assignment_source",
            "is_active",
        )

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        """
        Validate the serializer data.
        """

        validate_role_permission(
            role=attrs["role"],
            permission=attrs["permission"],
            assignment_type=attrs["assignment_type"],
            assignment_source=attrs["assignment_source"],
        )

        return attrs

    def create(
        self,
        validated_data: dict,
    ) -> RolePermission:
        """
        Create a role permission.
        """

        return create_role_permission(
            validated_data=validated_data,
        )
