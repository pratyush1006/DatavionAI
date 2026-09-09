"""
Billing Core RBAC adapters.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class BillingPermission:
    """Stable Billing Core permission identifiers."""

    LIST = "billing.list"
    VIEW = "billing.view"
    INVOICE_CREATE = "billing.invoice.create"
    INVOICE_UPDATE = "billing.invoice.update"
    INVOICE_DELETE = "billing.invoice.delete"
    INVOICE_VOID = "billing.invoice.void"
    PAYMENT_CREATE = "billing.payment.create"
    CLAIM_CREATE = "billing.claim.create"
    CLAIM_APPROVE = "billing.claim.approve"
    CLAIM_REJECT = "billing.claim.reject"
    CLAIM_APPEAL = "billing.claim.appeal"
    CLAIM_SETTLE = "billing.claim.settle"


class CanListBilling(RBACPermissionBase):
    """Require Billing list permission."""

    permission_code = BillingPermission.LIST
    message = "You do not have permission to list billing records."


class CanViewBilling(RBACPermissionBase):
    """Require Billing view permission."""

    permission_code = BillingPermission.VIEW
    message = "You do not have permission to view billing records."


class CanCreateInvoice(RBACPermissionBase):
    """Require invoice creation permission."""

    permission_code = BillingPermission.INVOICE_CREATE
    message = "You do not have permission to create invoices."


class CanUpdateInvoice(RBACPermissionBase):
    """Require invoice update permission."""

    permission_code = BillingPermission.INVOICE_UPDATE
    message = "You do not have permission to update invoices."


class CanDeleteInvoice(RBACPermissionBase):
    """Require invoice deletion permission."""

    permission_code = BillingPermission.INVOICE_DELETE
    message = "You do not have permission to delete invoices."


class CanVoidInvoice(RBACPermissionBase):
    """Require invoice void permission."""

    permission_code = BillingPermission.INVOICE_VOID
    message = "You do not have permission to void invoices."


class CanProcessPayment(RBACPermissionBase):
    """Require payment processing permission."""

    permission_code = BillingPermission.PAYMENT_CREATE
    message = "You do not have permission to process payments."


class CanSubmitClaim(RBACPermissionBase):
    """Require claim submission permission."""

    permission_code = BillingPermission.CLAIM_CREATE
    message = "You do not have permission to submit insurance claims."


class CanApproveClaim(RBACPermissionBase):
    """Require claim approval permission."""

    permission_code = BillingPermission.CLAIM_APPROVE
    message = "You do not have permission to approve insurance claims."


class CanRejectClaim(RBACPermissionBase):
    """Require claim rejection permission."""

    permission_code = BillingPermission.CLAIM_REJECT
    message = "You do not have permission to reject insurance claims."


class CanAppealClaim(RBACPermissionBase):
    """Require claim appeal permission."""

    permission_code = BillingPermission.CLAIM_APPEAL
    message = "You do not have permission to appeal insurance claims."


class CanSettleClaim(RBACPermissionBase):
    """Require claim settlement permission."""

    permission_code = BillingPermission.CLAIM_SETTLE
    message = "You do not have permission to settle insurance claims."


__all__ = (
    "BillingPermission",
    "CanAppealClaim",
    "CanApproveClaim",
    "CanCreateInvoice",
    "CanDeleteInvoice",
    "CanListBilling",
    "CanProcessPayment",
    "CanRejectClaim",
    "CanSettleClaim",
    "CanSubmitClaim",
    "CanUpdateInvoice",
    "CanViewBilling",
    "CanVoidInvoice",
)
