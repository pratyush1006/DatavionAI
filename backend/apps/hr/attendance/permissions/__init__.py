"""
Attendance permission classes.
"""

from .attendance_record import (
    CanCreateAttendance,
    CanDeleteAttendance,
    CanUpdateAttendance,
    CanViewAttendance,
)

__all__ = [
    "CanViewAttendance",
    "CanCreateAttendance",
    "CanUpdateAttendance",
    "CanDeleteAttendance",
]
