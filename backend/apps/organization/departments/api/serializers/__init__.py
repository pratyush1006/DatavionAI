"""
Department serializer exports.
"""

from .base import DepartmentBaseSerializer
from .create import DepartmentCreateSerializer
from .detail import DepartmentDetailSerializer
from .list import DepartmentListSerializer
from .update import DepartmentUpdateSerializer

__all__ = [
    "DepartmentBaseSerializer",
    "DepartmentCreateSerializer",
    "DepartmentDetailSerializer",
    "DepartmentListSerializer",
    "DepartmentUpdateSerializer",
]
