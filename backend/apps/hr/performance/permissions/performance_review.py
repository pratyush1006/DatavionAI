"""
Performance review permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewPerformanceReview(DatavionPermission):
    permission_code = "performance.view"


class CanCreatePerformanceReview(DatavionPermission):
    permission_code = "performance.create"


class CanUpdatePerformanceReview(DatavionPermission):
    permission_code = "performance.update"


class CanDeletePerformanceReview(DatavionPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewPerformanceReview",
    "CanCreatePerformanceReview",
    "CanUpdatePerformanceReview",
    "CanDeletePerformanceReview",
]
