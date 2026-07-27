"""
Lifecycle process permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewLifecycleProcess(DatavionPermission):
    permission_code = "onboarding.view"


class CanCreateLifecycleProcess(DatavionPermission):
    permission_code = "onboarding.create"


class CanUpdateLifecycleProcess(DatavionPermission):
    permission_code = "onboarding.update"


class CanDeleteLifecycleProcess(DatavionPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewLifecycleProcess",
    "CanCreateLifecycleProcess",
    "CanUpdateLifecycleProcess",
    "CanDeleteLifecycleProcess",
]
