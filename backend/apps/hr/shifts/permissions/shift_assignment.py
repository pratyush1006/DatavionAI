"""
Shift assignment permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewShiftAssignment(HrPermission):
    permission_code = "shifts.view"


class CanCreateShiftAssignment(HrPermission):
    permission_code = "shifts.create"


class CanUpdateShiftAssignment(HrPermission):
    permission_code = "shifts.update"


class CanDeleteShiftAssignment(HrPermission):
    permission_code = "shifts.delete"


class CanAssignShift(HrPermission):
    permission_code = "shifts.assign"


__all__ = [
    "CanViewShiftAssignment",
    "CanCreateShiftAssignment",
    "CanUpdateShiftAssignment",
    "CanDeleteShiftAssignment",
    "CanAssignShift",
]
