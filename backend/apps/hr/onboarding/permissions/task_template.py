"""
Lifecycle task template permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewTaskTemplate(DatavionPermission):
    permission_code = "onboarding.view"


class CanCreateTaskTemplate(DatavionPermission):
    permission_code = "onboarding.create"


class CanUpdateTaskTemplate(DatavionPermission):
    permission_code = "onboarding.update"


class CanDeleteTaskTemplate(DatavionPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewTaskTemplate",
    "CanCreateTaskTemplate",
    "CanUpdateTaskTemplate",
    "CanDeleteTaskTemplate",
]
