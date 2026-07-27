"""
Department selectors.
"""

from __future__ import annotations

from apps.organization.departments.selectors.department import (
    DepartmentSelector,
    get_department_by_id,
    get_departments,
)

__all__ = [
    "DepartmentSelector",
    "get_departments",
    "get_department_by_id",
]
