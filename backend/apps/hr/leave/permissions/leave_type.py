"""
Leave type permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewLeaveType(HrPermission):
    permission_code = "leave.view"


class CanCreateLeaveType(HrPermission):
    permission_code = "leave.create"


class CanUpdateLeaveType(HrPermission):
    permission_code = "leave.update"


class CanDeleteLeaveType(HrPermission):
    permission_code = "leave.delete"


__all__ = [
    "CanViewLeaveType",
    "CanCreateLeaveType",
    "CanUpdateLeaveType",
    "CanDeleteLeaveType",
]
