"""
Department API views.
"""

from .list_create import DepartmentListCreateAPIView
from .retrieve_update_destroy import (
    DepartmentRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "DepartmentListCreateAPIView",
    "DepartmentRetrieveUpdateDestroyAPIView",
]
