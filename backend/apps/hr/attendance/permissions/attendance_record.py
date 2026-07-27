"""
Attendance permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewAttendance(DatavionPermission):
    permission_code = "attendance.view"


class CanCreateAttendance(DatavionPermission):
    permission_code = "attendance.create"


class CanUpdateAttendance(DatavionPermission):
    permission_code = "attendance.update"


class CanDeleteAttendance(DatavionPermission):
    permission_code = "attendance.delete"


__all__ = [
    "CanViewAttendance",
    "CanCreateAttendance",
    "CanUpdateAttendance",
    "CanDeleteAttendance",
]
