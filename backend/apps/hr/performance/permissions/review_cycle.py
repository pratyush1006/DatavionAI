"""
Performance review cycle permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewReviewCycle(DatavionPermission):
    permission_code = "performance.view"


class CanCreateReviewCycle(DatavionPermission):
    permission_code = "performance.create"


class CanUpdateReviewCycle(DatavionPermission):
    permission_code = "performance.update"


class CanDeleteReviewCycle(DatavionPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewReviewCycle",
    "CanCreateReviewCycle",
    "CanUpdateReviewCycle",
    "CanDeleteReviewCycle",
]
