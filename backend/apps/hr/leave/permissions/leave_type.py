"""
Leave type permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewLeaveType(DatavionPermission):
    permission_code = "leave.view"


class CanCreateLeaveType(DatavionPermission):
    permission_code = "leave.create"


class CanUpdateLeaveType(DatavionPermission):
    permission_code = "leave.update"


class CanDeleteLeaveType(DatavionPermission):
    permission_code = "leave.delete"


__all__ = [
    "CanViewLeaveType",
    "CanCreateLeaveType",
    "CanUpdateLeaveType",
    "CanDeleteLeaveType",
]
