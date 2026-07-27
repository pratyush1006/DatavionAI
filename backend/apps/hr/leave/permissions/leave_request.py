"""
Leave request permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewLeaveRequest(DatavionPermission):
    permission_code = "leave.view"


class CanCreateLeaveRequest(DatavionPermission):
    permission_code = "leave.create"


class CanUpdateLeaveRequest(DatavionPermission):
    permission_code = "leave.update"


class CanDeleteLeaveRequest(DatavionPermission):
    permission_code = "leave.delete"


class CanApproveLeaveRequest(DatavionPermission):
    permission_code = "leave.approve"


__all__ = [
    "CanViewLeaveRequest",
    "CanCreateLeaveRequest",
    "CanUpdateLeaveRequest",
    "CanDeleteLeaveRequest",
    "CanApproveLeaveRequest",
]
