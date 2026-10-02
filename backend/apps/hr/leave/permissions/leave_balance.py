"""
Leave balance permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewLeaveBalance(HrPermission):
    permission_code = "leave.view"


class CanCreateLeaveBalance(HrPermission):
    permission_code = "leave.create"


class CanUpdateLeaveBalance(HrPermission):
    permission_code = "leave.update"


class CanDeleteLeaveBalance(HrPermission):
    permission_code = "leave.delete"


__all__ = [
    "CanViewLeaveBalance",
    "CanCreateLeaveBalance",
    "CanUpdateLeaveBalance",
    "CanDeleteLeaveBalance",
]
