"""
Shift permission classes.
"""

from .shift import (
    CanCreateShift,
    CanDeleteShift,
    CanUpdateShift,
    CanViewShift,
)
from .shift_assignment import (
    CanAssignShift,
    CanCreateShiftAssignment,
    CanDeleteShiftAssignment,
    CanUpdateShiftAssignment,
    CanViewShiftAssignment,
)

__all__ = [
    "CanViewShift",
    "CanCreateShift",
    "CanUpdateShift",
    "CanDeleteShift",
    "CanViewShiftAssignment",
    "CanCreateShiftAssignment",
    "CanUpdateShiftAssignment",
    "CanDeleteShiftAssignment",
    "CanAssignShift",
]
