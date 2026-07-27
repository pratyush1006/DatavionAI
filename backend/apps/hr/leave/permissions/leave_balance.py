"""
Leave balance permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewLeaveBalance(DatavionPermission):
    permission_code = "leave.view"


class CanCreateLeaveBalance(DatavionPermission):
    permission_code = "leave.create"


class CanUpdateLeaveBalance(DatavionPermission):
    permission_code = "leave.update"


class CanDeleteLeaveBalance(DatavionPermission):
    permission_code = "leave.delete"


__all__ = [
    "CanViewLeaveBalance",
    "CanCreateLeaveBalance",
    "CanUpdateLeaveBalance",
    "CanDeleteLeaveBalance",
]
