"""
Performance review cycle permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewReviewCycle(HrPermission):
    permission_code = "performance.view"


class CanCreateReviewCycle(HrPermission):
    permission_code = "performance.create"


class CanUpdateReviewCycle(HrPermission):
    permission_code = "performance.update"


class CanDeleteReviewCycle(HrPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewReviewCycle",
    "CanCreateReviewCycle",
    "CanUpdateReviewCycle",
    "CanDeleteReviewCycle",
]
