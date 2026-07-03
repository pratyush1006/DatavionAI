"""
Serializer field definitions for Employees.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee_code",
    "employee_name",
    "designation",
    "organization",
    "department",
    "team",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee_code",
    "employee_name",
    "user_id",
    "organization",
    "organization_id",
    "department",
    "department_id",
    "team",
    "team_id",
    "designation",
    "manager",
    "manager_id",
    "hire_date",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "department",
    "team",
    "user",
    "employee_code",
    "designation",
    "manager",
    "hire_date",
    "is_active",
)

UPDATE_FIELDS = WRITE_FIELDS

__all__ = [
    "LIST_FIELDS",
    "DETAIL_FIELDS",
    "WRITE_FIELDS",
    "UPDATE_FIELDS",
]
