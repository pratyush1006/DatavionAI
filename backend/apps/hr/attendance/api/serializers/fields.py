"""
Serializer field definitions for Attendance.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "work_date",
    "check_in",
    "check_out",
    "hours_worked",
    "status",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "work_date",
    "check_in",
    "check_out",
    "hours_worked",
    "status",
    "notes",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "work_date",
    "check_in",
    "check_out",
    "status",
    "notes",
)

UPDATE_FIELDS = WRITE_FIELDS

__all__ = [
    "LIST_FIELDS",
    "DETAIL_FIELDS",
    "WRITE_FIELDS",
    "UPDATE_FIELDS",
]
