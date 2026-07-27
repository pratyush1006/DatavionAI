"""
Database selectors for the Attendance app.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.hr.attendance.models import AttendanceRecord


def get_attendance_records() -> QuerySet[AttendanceRecord]:
    """
    Return all attendance records with related objects.
    """

    return AttendanceRecord.objects.select_related(
        "organization",
        "employee",
        "employee__user",
    )


def get_attendance_record_by_id(
    *,
    attendance_record_id: int,
) -> AttendanceRecord:
    """
    Return an attendance record by ID.
    """

    return get_object_or_404(
        get_attendance_records(),
        pk=attendance_record_id,
    )


__all__ = [
    "get_attendance_records",
    "get_attendance_record_by_id",
]
