"""
Role hierarchy create serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    RoleHierarchy,
)
from rest_framework import serializers


class RoleHierarchyCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating role hierarchies.
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
    "RoleHierarchyCreateSerializer",
]
