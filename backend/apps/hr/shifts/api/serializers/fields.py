"""
Serializer field definitions for Shifts.
"""

from __future__ import annotations

from typing import Final

SHIFT_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "code",
    "start_time",
    "end_time",
    "is_night_shift",
    "is_active",
)

SHIFT_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "name",
    "code",
    "start_time",
    "end_time",
    "break_minutes",
    "is_night_shift",
    "is_active",
    "created_at",
    "updated_at",
)

SHIFT_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "code",
    "start_time",
    "end_time",
    "break_minutes",
    "is_night_shift",
    "is_active",
)

SHIFT_ASSIGNMENT_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "shift",
    "work_date",
    "status",
)

SHIFT_ASSIGNMENT_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "shift",
    "shift_id",
    "work_date",
    "status",
    "notes",
    "created_at",
    "updated_at",
)

SHIFT_ASSIGNMENT_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "shift",
    "work_date",
    "status",
    "notes",
)

__all__ = [
    "SHIFT_LIST_FIELDS",
    "SHIFT_DETAIL_FIELDS",
    "SHIFT_WRITE_FIELDS",
    "SHIFT_ASSIGNMENT_LIST_FIELDS",
    "SHIFT_ASSIGNMENT_DETAIL_FIELDS",
    "SHIFT_ASSIGNMENT_WRITE_FIELDS",
]
