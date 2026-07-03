"""
Employee permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewEmployee(DatavionPermission):
    permission_code = "employee.view"


class CanCreateEmployee(DatavionPermission):
    permission_code = "employee.create"


class CanUpdateEmployee(DatavionPermission):
    permission_code = "employee.update"


class CanDeleteEmployee(DatavionPermission):
    permission_code = "employee.delete"


__all__ = [
    "CanViewEmployee",
    "CanCreateEmployee",
    "CanUpdateEmployee",
    "CanDeleteEmployee",
]
