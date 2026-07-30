"""
Role update serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.services import (
    update_role,
)
from rest_framework import serializers


class RoleUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating a role.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = Role

        fields = (
            "name",
            "description",
            "role_type",
            "scope",
            "category",
            "parent",
            "priority",
            "display_order",
            "is_system",
            "is_default",
            "is_assignable",
            "is_editable",
            "is_deletable",
            "is_active",
        )

    def update(
        self,
        instance: Role,
        validated_data: dict,
    ) -> Role:
        """
        Update and return a role.
        """

        return update_role(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "RoleUpdateSerializer",
]
