"""
Employee selectors.

Central export point for employee read/query operations.
"""

from __future__ import annotations

from apps.organization.employees.selectors.employee import (
    EmployeeSelector,
    get_active_employees,
    get_employee,
    get_employee_by_id,
    get_employees,
)

__all__ = (
    "EmployeeSelector",
    "get_employees",
    "get_employee",
    "get_employee_by_id",
    "get_active_employees",
)
