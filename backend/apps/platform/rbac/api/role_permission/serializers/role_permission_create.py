"""
Role permission create serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
    RolePermissionSource,
    RolePermissionType,
)
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

    assignment_type = serializers.ChoiceField(
        choices=RolePermissionType.choices,
        required=False,
        default=DEFAULT_ROLE_PERMISSION_TYPE,
    )

    assignment_source = serializers.ChoiceField(
        choices=RolePermissionSource.choices,
        required=False,
        default=DEFAULT_ROLE_PERMISSION_SOURCE,
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

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        """
        Validate role permission assignment.
        """

        validate_role_permission(
            role=attrs["role"],
            permission=attrs["permission"],
            assignment_type=attrs.get(
                "assignment_type",
                DEFAULT_ROLE_PERMISSION_TYPE,
            ),
            assignment_source=attrs.get(
                "assignment_source",
                DEFAULT_ROLE_PERMISSION_SOURCE,
            ),
        )

        return attrs

    def create(
        self,
        validated_data: dict,
    ) -> RolePermission:
        """
        Create role permission.
        """

        return create_role_permission(
            validated_data=validated_data,
        )


__all__ = [
    "RolePermissionCreateSerializer",
]
