"""
Lifecycle task permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewLifecycleTask(HrPermission):
    permission_code = "onboarding.view"


class CanCreateLifecycleTask(HrPermission):
    permission_code = "onboarding.create"


class CanUpdateLifecycleTask(HrPermission):
    permission_code = "onboarding.update"


class CanDeleteLifecycleTask(HrPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewLifecycleTask",
    "CanCreateLifecycleTask",
    "CanUpdateLifecycleTask",
    "CanDeleteLifecycleTask",
]
