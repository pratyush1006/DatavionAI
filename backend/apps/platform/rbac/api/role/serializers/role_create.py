"""
Role create serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import Role
from apps.platform.rbac.services import create_role
from rest_framework import serializers


class RoleCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a role.
    """

    class Meta:
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
        )

    def create(
        self,
        validated_data: dict,
    ) -> Role:
        return create_role(
            validated_data=validated_data,
        )


__all__ = [
    "RoleCreateSerializer",
]
