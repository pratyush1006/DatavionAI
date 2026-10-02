"""
Payslip permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewPayslip(HrPermission):
    permission_code = "payroll.view"


class CanCreatePayslip(HrPermission):
    permission_code = "payroll.create"


class CanUpdatePayslip(HrPermission):
    permission_code = "payroll.update"


class CanDeletePayslip(HrPermission):
    permission_code = "payroll.delete"


class CanProcessPayslip(HrPermission):
    permission_code = "payroll.verify"


class CanReleasePayslip(HrPermission):
    permission_code = "payroll.release"


__all__ = [
    "CanViewPayslip",
    "CanCreatePayslip",
    "CanUpdatePayslip",
    "CanDeletePayslip",
    "CanProcessPayslip",
    "CanReleasePayslip",
]
