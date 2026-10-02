"""
Role hierarchy update serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.rbac.models import (
    RoleHierarchy,
)


class RoleHierarchyUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating role hierarchies.
    """

    class Meta:
        model = RoleHierarchy

        fields = (
            "parent_role",
            "child_role",
            "hierarchy_type",
            "assignment_source",
            "is_active",
        )


__all__ = [
    "RoleHierarchyUpdateSerializer",
]
