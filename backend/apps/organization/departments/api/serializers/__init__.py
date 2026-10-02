"""
Department serializer exports.
"""

from __future__ import annotations

from apps.organization.departments.api.serializers.base import (
    DepartmentBaseSerializer,
)
from apps.organization.departments.api.serializers.create import (
    DepartmentCreateSerializer,
)
from apps.organization.departments.api.serializers.detail import (
    DepartmentDetailSerializer,
)
from apps.organization.departments.api.serializers.list import (
    DepartmentListSerializer,
)
from apps.organization.departments.api.serializers.update import (
    DepartmentUpdateSerializer,
)

__all__ = [
    "DepartmentBaseSerializer",
    "DepartmentCreateSerializer",
    "DepartmentDetailSerializer",
    "DepartmentListSerializer",
    "DepartmentUpdateSerializer",
]
