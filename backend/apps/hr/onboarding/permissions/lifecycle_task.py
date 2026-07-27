"""
Lifecycle task permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewLifecycleTask(DatavionPermission):
    permission_code = "onboarding.view"


class CanCreateLifecycleTask(DatavionPermission):
    permission_code = "onboarding.create"


class CanUpdateLifecycleTask(DatavionPermission):
    permission_code = "onboarding.update"


class CanDeleteLifecycleTask(DatavionPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewLifecycleTask",
    "CanCreateLifecycleTask",
    "CanUpdateLifecycleTask",
    "CanDeleteLifecycleTask",
]
