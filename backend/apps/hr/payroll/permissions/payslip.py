"""
Payslip permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewPayslip(DatavionPermission):
    permission_code = "payroll.view"


class CanCreatePayslip(DatavionPermission):
    permission_code = "payroll.create"


class CanUpdatePayslip(DatavionPermission):
    permission_code = "payroll.update"


class CanDeletePayslip(DatavionPermission):
    permission_code = "payroll.delete"


class CanProcessPayslip(DatavionPermission):
    permission_code = "payroll.verify"


class CanReleasePayslip(DatavionPermission):
    permission_code = "payroll.release"


__all__ = [
    "CanViewPayslip",
    "CanCreatePayslip",
    "CanUpdatePayslip",
    "CanDeletePayslip",
    "CanProcessPayslip",
    "CanReleasePayslip",
]
