"""
Organization role update serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    OrganizationRole,
)


class OrganizationRoleUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating organization role assignments.
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
    "OrganizationRoleUpdateSerializer",
]
