"""
Attendance constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class AttendanceStatus(TextChoices):
    """
    Attendance status choices for a single work day.
    """

    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    HALF_DAY = "half_day", "Half Day"
    LATE = "late", "Late"
    ON_LEAVE = "on_leave", "On Leave"
    HOLIDAY = "holiday", "Holiday"
    WEEK_OFF = "week_off", "Week Off"


DEFAULT_ATTENDANCE_STATUS = AttendanceStatus.PRESENT


__all__ = [
    "AttendanceStatus",
    "DEFAULT_ATTENDANCE_STATUS",
]
