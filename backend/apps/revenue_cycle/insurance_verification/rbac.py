"""DRF RBAC adapters for Insurance Verification."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase
from apps.revenue_cycle.insurance_verification.permissions import (
    InsuranceVerificationPermission,
)


class CanViewInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification view permission."""

    permission_code = InsuranceVerificationPermission.VIEW
    message = "You do not have permission to view insurance verification records."


class CanCreateInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification creation permission."""

    permission_code = InsuranceVerificationPermission.CREATE
    message = "You do not have permission to create insurance verification records."


class CanUpdateInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification update permission."""

    permission_code = InsuranceVerificationPermission.UPDATE
    message = "You do not have permission to update insurance verification records."


class CanDeleteInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification deletion permission."""

    permission_code = InsuranceVerificationPermission.DELETE
    message = "You do not have permission to delete insurance verification records."


class CanRestoreInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification restoration permission."""

    permission_code = InsuranceVerificationPermission.RESTORE
    message = "You do not have permission to restore insurance verification records."


class CanTransitionInsuranceVerification(RBACPermissionBase):
    """Require Insurance Verification lifecycle permission."""

    permission_code = InsuranceVerificationPermission.LIFECYCLE
    message = "You do not have permission to change insurance verification lifecycle."


__all__ = (
    "CanCreateInsuranceVerification",
    "CanDeleteInsuranceVerification",
    "CanRestoreInsuranceVerification",
    "CanTransitionInsuranceVerification",
    "CanUpdateInsuranceVerification",
    "CanViewInsuranceVerification",
)
