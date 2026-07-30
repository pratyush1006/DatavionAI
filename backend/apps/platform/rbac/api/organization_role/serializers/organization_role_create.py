"""
Organization role create serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    OrganizationRole,
)
from rest_framework import serializers


class OrganizationRoleCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating organization role assignments.
    """

    class Meta:
        model = OrganizationRole

        fields = (
            "organization",
            "user",
            "role",
            "assignment_source",
            "is_primary",
            "is_active",
        )


__all__ = [
    "OrganizationRoleCreateSerializer",
]
