"""
Performance review permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewPerformanceReview(HrPermission):
    permission_code = "performance.view"


class CanCreatePerformanceReview(HrPermission):
    permission_code = "performance.create"


class CanUpdatePerformanceReview(HrPermission):
    permission_code = "performance.update"


class CanDeletePerformanceReview(HrPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewPerformanceReview",
    "CanCreatePerformanceReview",
    "CanUpdatePerformanceReview",
    "CanDeletePerformanceReview",
]
