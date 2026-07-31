"""
Organization role detail serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    OrganizationRole,
)


class OrganizationRoleDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for organization role details.
    """

    class Meta:
        model = OrganizationRole

        fields = (
            "id",
            "organization",
            "user",
            "role",
            "assignment_source",
            "is_primary",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
        )


__all__ = [
    "OrganizationRoleDetailSerializer",
]
