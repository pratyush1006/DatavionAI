"""
Salary structure permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewSalaryStructure(HrPermission):
    permission_code = "payroll.view"


class CanCreateSalaryStructure(HrPermission):
    permission_code = "payroll.create"


class CanUpdateSalaryStructure(HrPermission):
    permission_code = "payroll.update"


class CanDeleteSalaryStructure(HrPermission):
    permission_code = "payroll.delete"


__all__ = [
    "CanViewSalaryStructure",
    "CanCreateSalaryStructure",
    "CanUpdateSalaryStructure",
    "CanDeleteSalaryStructure",
]
