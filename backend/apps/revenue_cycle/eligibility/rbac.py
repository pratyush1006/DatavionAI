"""DRF RBAC adapters for Eligibility."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase
from apps.revenue_cycle.eligibility.permissions import EligibilityPermission


class CanViewEligibility(RBACPermissionBase):
    """Require Eligibility view permission."""

    permission_code = EligibilityPermission.VIEW
    message = "You do not have permission to view eligibility records."


class CanCreateEligibility(RBACPermissionBase):
    """Require Eligibility creation permission."""

    permission_code = EligibilityPermission.CREATE
    message = "You do not have permission to create eligibility records."


class CanUpdateEligibility(RBACPermissionBase):
    """Require Eligibility update permission."""

    permission_code = EligibilityPermission.UPDATE
    message = "You do not have permission to update eligibility records."


class CanDeleteEligibility(RBACPermissionBase):
    """Require Eligibility deletion permission."""

    permission_code = EligibilityPermission.DELETE
    message = "You do not have permission to delete eligibility records."


class CanRestoreEligibility(RBACPermissionBase):
    """Require Eligibility restoration permission."""

    permission_code = EligibilityPermission.RESTORE
    message = "You do not have permission to restore eligibility records."


class CanTransitionEligibility(RBACPermissionBase):
    """Require Eligibility lifecycle permission."""

    permission_code = EligibilityPermission.LIFECYCLE
    message = "You do not have permission to change eligibility lifecycle."


__all__ = (
    "CanCreateEligibility",
    "CanDeleteEligibility",
    "CanRestoreEligibility",
    "CanTransitionEligibility",
    "CanUpdateEligibility",
    "CanViewEligibility",
)
