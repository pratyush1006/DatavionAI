"""
Holiday permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewHoliday(HrPermission):
    permission_code = "holidays.view"


class CanCreateHoliday(HrPermission):
    permission_code = "holidays.create"


class CanUpdateHoliday(HrPermission):
    permission_code = "holidays.update"


class CanDeleteHoliday(HrPermission):
    permission_code = "holidays.delete"


__all__ = [
    "CanViewHoliday",
    "CanCreateHoliday",
    "CanUpdateHoliday",
    "CanDeleteHoliday",
]
