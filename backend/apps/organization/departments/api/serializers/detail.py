"""
Detail serializer for Departments.
"""

from __future__ import annotations

from .base import DepartmentBaseSerializer
from .fields import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class DepartmentDetailSerializer(
    DepartmentBaseSerializer,
):
    class Meta(
        DepartmentBaseSerializer.Meta,
    ):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "DepartmentDetailSerializer",
]
