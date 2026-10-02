"""
Shift permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewShift(HrPermission):
    permission_code = "shifts.view"


class CanCreateShift(HrPermission):
    permission_code = "shifts.create"


class CanUpdateShift(HrPermission):
    permission_code = "shifts.update"


class CanDeleteShift(HrPermission):
    permission_code = "shifts.delete"


__all__ = [
    "CanViewShift",
    "CanCreateShift",
    "CanUpdateShift",
    "CanDeleteShift",
]
