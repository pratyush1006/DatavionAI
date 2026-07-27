"""
Permission classes for the Eligibility Check module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class EligibilityCheckPermission:
    VIEW = "eligibility.view"
    CREATE = "eligibility.create"
    UPDATE = "eligibility.update"
    DELETE = "eligibility.delete"


class CanViewEligibilityCheck(BasePermission):
    permission_code = EligibilityCheckPermission.VIEW


class CanCreateEligibilityCheck(BasePermission):
    permission_code = EligibilityCheckPermission.CREATE


class CanUpdateEligibilityCheck(BasePermission):
    permission_code = EligibilityCheckPermission.UPDATE


class CanDeleteEligibilityCheck(BasePermission):
    permission_code = EligibilityCheckPermission.DELETE


__all__ = [
    "CanCreateEligibilityCheck",
    "CanDeleteEligibilityCheck",
    "CanUpdateEligibilityCheck",
    "CanViewEligibilityCheck",
    "EligibilityCheckPermission",
]
