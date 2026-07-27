"""
Holiday permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewHoliday(DatavionPermission):
    permission_code = "holidays.view"


class CanCreateHoliday(DatavionPermission):
    permission_code = "holidays.create"


class CanUpdateHoliday(DatavionPermission):
    permission_code = "holidays.update"


class CanDeleteHoliday(DatavionPermission):
    permission_code = "holidays.delete"


__all__ = [
    "CanViewHoliday",
    "CanCreateHoliday",
    "CanUpdateHoliday",
    "CanDeleteHoliday",
]
