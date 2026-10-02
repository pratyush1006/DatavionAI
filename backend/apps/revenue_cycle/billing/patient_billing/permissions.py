"""Patient Billing RBAC adapters."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanListPatientBillingAccounts(RBACPermissionBase):
    """Require patient billing account view permission."""

    permission_code = "billing.patient_account.view"
    message = "You do not have permission to view patient billing accounts."


class CanCreatePatientBillingAccount(RBACPermissionBase):
    """Require patient billing account creation permission."""

    permission_code = "billing.patient_account.create"
    message = "You do not have permission to create patient billing accounts."


class CanUpdatePatientBillingAccount(RBACPermissionBase):
    """Require patient billing account update permission."""

    permission_code = "billing.patient_account.update"
    message = "You do not have permission to update patient billing accounts."


class CanTransitionPatientBillingAccount(RBACPermissionBase):
    """Require patient billing account lifecycle permission."""

    permission_code = "billing.patient_account.lifecycle"
    message = "You do not have permission to change account lifecycle."


class CanViewPatientGuarantor(RBACPermissionBase):
    """Require guarantor view permission."""

    permission_code = "billing.guarantor.view"
    message = "You do not have permission to view guarantors."


class CanCreatePatientGuarantor(RBACPermissionBase):
    """Require guarantor create permission."""

    permission_code = "billing.guarantor.create"
    message = "You do not have permission to create guarantors."


class CanUpdatePatientGuarantor(RBACPermissionBase):
    """Require guarantor update permission."""

    permission_code = "billing.guarantor.update"
    message = "You do not have permission to update guarantors."


class CanDeletePatientGuarantor(RBACPermissionBase):
    """Require guarantor delete permission."""

    permission_code = "billing.guarantor.delete"
    message = "You do not have permission to delete guarantors."


class CanRestorePatientGuarantor(RBACPermissionBase):
    """Require guarantor restore permission."""

    permission_code = "billing.guarantor.restore"
    message = "You do not have permission to restore guarantors."


class CanViewPatientResponsibility(RBACPermissionBase):
    """Require responsibility view permission."""

    permission_code = "billing.responsibility.view"
    message = "You do not have permission to view responsibility records."


class CanCreatePatientResponsibility(RBACPermissionBase):
    """Require responsibility create permission."""

    permission_code = "billing.responsibility.create"
    message = "You do not have permission to create responsibility records."


class CanUpdatePatientResponsibility(RBACPermissionBase):
    """Require responsibility update permission."""

    permission_code = "billing.responsibility.update"
    message = "You do not have permission to update responsibility records."


class CanDeletePatientResponsibility(RBACPermissionBase):
    """Require responsibility delete permission."""

    permission_code = "billing.responsibility.delete"
    message = "You do not have permission to delete responsibility records."


class CanRestorePatientResponsibility(RBACPermissionBase):
    """Require responsibility restore permission."""

    permission_code = "billing.responsibility.restore"
    message = "You do not have permission to restore responsibility records."


class CanViewPatientStatement(RBACPermissionBase):
    """Require patient statement view permission."""

    permission_code = "billing.statement.view"
    message = "You do not have permission to view patient statements."


class CanCreatePatientStatement(RBACPermissionBase):
    """Require patient statement creation permission."""

    permission_code = "billing.statement.create"
    message = "You do not have permission to create patient statements."


class CanIssuePatientStatement(RBACPermissionBase):
    """Require patient statement issue permission."""

    permission_code = "billing.statement.issue"
    message = "You do not have permission to issue patient statements."


class CanVoidPatientStatement(RBACPermissionBase):
    """Require patient statement void permission."""

    permission_code = "billing.statement.void"
    message = "You do not have permission to void patient statements."


__all__ = (
    "CanCreatePatientBillingAccount",
    "CanCreatePatientGuarantor",
    "CanCreatePatientResponsibility",
    "CanCreatePatientStatement",
    "CanDeletePatientGuarantor",
    "CanDeletePatientResponsibility",
    "CanIssuePatientStatement",
    "CanListPatientBillingAccounts",
    "CanRestorePatientGuarantor",
    "CanRestorePatientResponsibility",
    "CanTransitionPatientBillingAccount",
    "CanUpdatePatientBillingAccount",
    "CanUpdatePatientGuarantor",
    "CanUpdatePatientResponsibility",
    "CanViewPatientGuarantor",
    "CanViewPatientResponsibility",
    "CanViewPatientStatement",
    "CanVoidPatientStatement",
)
