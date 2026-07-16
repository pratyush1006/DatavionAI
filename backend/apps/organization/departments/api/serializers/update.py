"""
Update serializer for Departments.
"""

from __future__ import annotations

from .base import DepartmentBaseSerializer
from .fields import UPDATE_FIELDS


class DepartmentUpdateSerializer(
    DepartmentBaseSerializer,
):
    class Meta(
        DepartmentBaseSerializer.Meta,
    ):
        fields = UPDATE_FIELDS


__all__ = [
    "DepartmentUpdateSerializer",
]
