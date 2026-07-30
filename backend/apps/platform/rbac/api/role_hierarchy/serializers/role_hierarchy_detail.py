"""
Role hierarchy detail serializer.
"""

from __future__ import annotations

from apps.platform.rbac.models import (
    RoleHierarchy,
)
from rest_framework import serializers


class RoleHierarchyDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for role hierarchy details.
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
            "updated_at",
            "is_deleted",
            "deleted_at",
        )


__all__ = [
    "RoleHierarchyDetailSerializer",
]
