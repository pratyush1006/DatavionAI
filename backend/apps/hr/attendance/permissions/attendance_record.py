"""
Attendance permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewAttendance(HrPermission):
    permission_code = "attendance.view"


class CanCreateAttendance(HrPermission):
    permission_code = "attendance.create"


class CanUpdateAttendance(HrPermission):
    permission_code = "attendance.update"


class CanDeleteAttendance(HrPermission):
    permission_code = "attendance.delete"


__all__ = [
    "CanViewAttendance",
    "CanCreateAttendance",
    "CanUpdateAttendance",
    "CanDeleteAttendance",
]
