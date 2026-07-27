"""
Performance goal permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewPerformanceGoal(DatavionPermission):
    permission_code = "performance.view"


class CanCreatePerformanceGoal(DatavionPermission):
    permission_code = "performance.create"


class CanUpdatePerformanceGoal(DatavionPermission):
    permission_code = "performance.update"


class CanDeletePerformanceGoal(DatavionPermission):
    permission_code = "performance.delete"


__all__ = [
    "CanViewPerformanceGoal",
    "CanCreatePerformanceGoal",
    "CanUpdatePerformanceGoal",
    "CanDeletePerformanceGoal",
]
