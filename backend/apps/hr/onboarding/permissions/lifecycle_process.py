"""
Lifecycle process permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewLifecycleProcess(HrPermission):
    permission_code = "onboarding.view"


class CanCreateLifecycleProcess(HrPermission):
    permission_code = "onboarding.create"


class CanUpdateLifecycleProcess(HrPermission):
    permission_code = "onboarding.update"


class CanDeleteLifecycleProcess(HrPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewLifecycleProcess",
    "CanCreateLifecycleProcess",
    "CanUpdateLifecycleProcess",
    "CanDeleteLifecycleProcess",
]
