"""
Shift API views.
"""

from .shift import (
    ShiftListCreateAPIView,
    ShiftRetrieveUpdateDestroyAPIView,
)
from .shift_assignment import (
    ShiftAssignmentListCreateAPIView,
    ShiftAssignmentRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "ShiftListCreateAPIView",
    "ShiftRetrieveUpdateDestroyAPIView",
    "ShiftAssignmentListCreateAPIView",
    "ShiftAssignmentRetrieveUpdateDestroyAPIView",
]
