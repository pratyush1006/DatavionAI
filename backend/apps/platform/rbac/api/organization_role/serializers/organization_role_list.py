"""
Organization role list serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    OrganizationRole,
)
from rest_framework import serializers


class OrganizationRoleListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing organization role assignments.
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
        )


__all__ = [
    "OrganizationRoleListSerializer",
]
