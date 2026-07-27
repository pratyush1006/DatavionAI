"""
Salary structure permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewSalaryStructure(DatavionPermission):
    permission_code = "payroll.view"


class CanCreateSalaryStructure(DatavionPermission):
    permission_code = "payroll.create"


class CanUpdateSalaryStructure(DatavionPermission):
    permission_code = "payroll.update"


class CanDeleteSalaryStructure(DatavionPermission):
    permission_code = "payroll.delete"


__all__ = [
    "CanViewSalaryStructure",
    "CanCreateSalaryStructure",
    "CanUpdateSalaryStructure",
    "CanDeleteSalaryStructure",
]
