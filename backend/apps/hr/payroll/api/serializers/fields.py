"""
Serializer field definitions for Payroll.
"""

from __future__ import annotations

from typing import Final

SALARY_STRUCTURE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "basic_salary",
    "gross_salary",
    "currency",
    "effective_from",
    "effective_to",
    "is_active",
)

SALARY_STRUCTURE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "basic_salary",
    "house_rent_allowance",
    "other_allowances",
    "gross_salary",
    "currency",
    "effective_from",
    "effective_to",
    "is_active",
    "created_at",
    "updated_at",
)

SALARY_STRUCTURE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "basic_salary",
    "house_rent_allowance",
    "other_allowances",
    "currency",
    "effective_from",
    "effective_to",
    "is_active",
)

PAYSLIP_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "pay_period_start",
    "pay_period_end",
    "net_pay",
    "currency",
    "status",
)

PAYSLIP_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "pay_period_start",
    "pay_period_end",
    "basic_salary",
    "total_allowances",
    "total_earnings",
    "total_deductions",
    "net_pay",
    "currency",
    "status",
    "paid_on",
    "notes",
    "line_items",
    "created_at",
    "updated_at",
)

PAYSLIP_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "pay_period_start",
    "pay_period_end",
    "basic_salary",
    "total_allowances",
    "currency",
    "notes",
    "line_items",
)

__all__ = [
    "SALARY_STRUCTURE_LIST_FIELDS",
    "SALARY_STRUCTURE_DETAIL_FIELDS",
    "SALARY_STRUCTURE_WRITE_FIELDS",
    "PAYSLIP_LIST_FIELDS",
    "PAYSLIP_DETAIL_FIELDS",
    "PAYSLIP_WRITE_FIELDS",
]
