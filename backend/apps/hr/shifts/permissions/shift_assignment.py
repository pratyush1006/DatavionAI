"""
Shift assignment permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewShiftAssignment(DatavionPermission):
    permission_code = "shifts.view"


class CanCreateShiftAssignment(DatavionPermission):
    permission_code = "shifts.create"


class CanUpdateShiftAssignment(DatavionPermission):
    permission_code = "shifts.update"


class CanDeleteShiftAssignment(DatavionPermission):
    permission_code = "shifts.delete"


class CanAssignShift(DatavionPermission):
    permission_code = "shifts.assign"


__all__ = [
    "CanViewShiftAssignment",
    "CanCreateShiftAssignment",
    "CanUpdateShiftAssignment",
    "CanDeleteShiftAssignment",
    "CanAssignShift",
]
