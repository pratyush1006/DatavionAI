"""
List serializer for Departments.
"""

from __future__ import annotations

from .base import DepartmentBaseSerializer
from .fields import LIST_FIELDS


class DepartmentListSerializer(
    DepartmentBaseSerializer,
):
    class Meta(
        DepartmentBaseSerializer.Meta,
    ):
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS


__all__ = [
    "DepartmentListSerializer",
]
