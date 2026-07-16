"""
Role hierarchy list serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    RoleHierarchy,
)
from rest_framework import serializers


class RoleHierarchyListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing role hierarchies.
    """

    class Meta:
        model = RoleHierarchy

        fields = (
            "id",
            "parent_role",
            "child_role",
            "hierarchy_type",
            "assignment_source",
            "is_active",
            "created_at",
        )


__all__ = [
    "RoleHierarchyListSerializer",
]
