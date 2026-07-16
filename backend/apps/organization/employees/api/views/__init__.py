"""
Employee API views.
"""

from .list_create import EmployeeListCreateAPIView
from .retrieve_update_destroy import (
    EmployeeRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "EmployeeListCreateAPIView",
    "EmployeeRetrieveUpdateDestroyAPIView",
]
