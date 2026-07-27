"""
Serializer field definitions for Leave.
"""

from __future__ import annotations

from typing import Final

LEAVE_TYPE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "code",
    "is_paid",
    "requires_approval",
    "max_days_per_year",
    "is_active",
)

LEAVE_TYPE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "name",
    "code",
    "description",
    "is_paid",
    "requires_approval",
    "max_days_per_year",
    "allow_carry_forward",
    "is_active",
    "created_at",
    "updated_at",
)

LEAVE_TYPE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "code",
    "description",
    "is_paid",
    "requires_approval",
    "max_days_per_year",
    "allow_carry_forward",
    "is_active",
)

LEAVE_BALANCE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "leave_type",
    "year",
    "allocated_days",
    "used_days",
    "remaining_days",
)

LEAVE_BALANCE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_id",
    "employee_name",
    "leave_type",
    "leave_type_id",
    "year",
    "allocated_days",
    "used_days",
    "carried_forward_days",
    "remaining_days",
    "created_at",
    "updated_at",
)

LEAVE_BALANCE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "employee",
    "leave_type",
    "year",
    "allocated_days",
    "used_days",
    "carried_forward_days",
)

LEAVE_REQUEST_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "leave_type",
    "start_date",
    "end_date",
    "number_of_days",
    "status",
)

LEAVE_REQUEST_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "leave_type",
    "leave_type_id",
    "start_date",
    "end_date",
    "number_of_days",
    "reason",
    "status",
    "approver",
    "approver_id",
    "decision_notes",
    "decided_at",
    "created_at",
    "updated_at",
)

LEAVE_REQUEST_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "leave_type",
    "start_date",
    "end_date",
    "number_of_days",
    "reason",
)

LEAVE_REQUEST_DECISION_FIELDS: Final[tuple[str, ...]] = ("decision_notes",)

__all__ = [
    "LEAVE_TYPE_LIST_FIELDS",
    "LEAVE_TYPE_DETAIL_FIELDS",
    "LEAVE_TYPE_WRITE_FIELDS",
    "LEAVE_BALANCE_LIST_FIELDS",
    "LEAVE_BALANCE_DETAIL_FIELDS",
    "LEAVE_BALANCE_WRITE_FIELDS",
    "LEAVE_REQUEST_LIST_FIELDS",
    "LEAVE_REQUEST_DETAIL_FIELDS",
    "LEAVE_REQUEST_WRITE_FIELDS",
    "LEAVE_REQUEST_DECISION_FIELDS",
]
