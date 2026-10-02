"""
Leave request permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewLeaveRequest(HrPermission):
    permission_code = "leave.view"


class CanCreateLeaveRequest(HrPermission):
    permission_code = "leave.create"


class CanUpdateLeaveRequest(HrPermission):
    permission_code = "leave.update"


class CanDeleteLeaveRequest(HrPermission):
    permission_code = "leave.delete"


class CanApproveLeaveRequest(HrPermission):
    permission_code = "leave.approve"


__all__ = [
    "CanViewLeaveRequest",
    "CanCreateLeaveRequest",
    "CanUpdateLeaveRequest",
    "CanDeleteLeaveRequest",
    "CanApproveLeaveRequest",
]
