"""
Shift permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewShift(DatavionPermission):
    permission_code = "shifts.view"


class CanCreateShift(DatavionPermission):
    permission_code = "shifts.create"


class CanUpdateShift(DatavionPermission):
    permission_code = "shifts.update"


class CanDeleteShift(DatavionPermission):
    permission_code = "shifts.delete"


__all__ = [
    "CanViewShift",
    "CanCreateShift",
    "CanUpdateShift",
    "CanDeleteShift",
]
