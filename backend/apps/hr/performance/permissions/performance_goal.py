"""
Performance goal permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewPerformanceGoal(HrPermission):
    permission_code = "performance.view"


class CanCreatePerformanceGoal(HrPermission):
    permission_code = "performance.create"


class CanUpdatePerformanceGoal(HrPermission):
    permission_code = "performance.update"


class CanDeletePerformanceGoal(HrPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewPerformanceGoal",
    "CanCreatePerformanceGoal",
    "CanUpdatePerformanceGoal",
    "CanDeletePerformanceGoal",
]
