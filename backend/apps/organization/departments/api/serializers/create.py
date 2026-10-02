"""
Create serializer for Departments.
"""

from __future__ import annotations

from .base import DepartmentBaseSerializer
from .fields import WRITE_FIELDS


class DepartmentCreateSerializer(
    DepartmentBaseSerializer,
):
    class Meta(
        DepartmentBaseSerializer.Meta,
    ):
        fields = WRITE_FIELDS


__all__ = [
    "DepartmentCreateSerializer",
]
