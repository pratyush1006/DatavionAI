"""
Lifecycle task template permission classes.
"""

from __future__ import annotations

from apps.hr.permissions import HrPermission


class CanViewTaskTemplate(HrPermission):
    permission_code = "onboarding.view"


class CanCreateTaskTemplate(HrPermission):
    permission_code = "onboarding.create"


class CanUpdateTaskTemplate(HrPermission):
    permission_code = "onboarding.update"


class CanDeleteTaskTemplate(HrPermission):
    permission_code = "onboarding.delete"


__all__ = [
    "CanViewTaskTemplate",
    "CanCreateTaskTemplate",
    "CanUpdateTaskTemplate",
    "CanDeleteTaskTemplate",
]
