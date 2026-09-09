"""Canonical explicit Billing permission codes."""

from __future__ import annotations


class BillingPermission:
    """Stable permission codes resolved by platform RBAC."""

    VIEW = "billing.view"
    CREATE = "billing.create"
    UPDATE = "billing.update"
    DELETE = "billing.delete"
    RESTORE = "billing.restore"
    ACTIVATE = "billing.activate"
    DEACTIVATE = "billing.deactivate"
    INVOICE_VIEW = "billing.invoice.view"
    INVOICE_CREATE = "billing.invoice.create"
    INVOICE_UPDATE = "billing.invoice.update"
    INVOICE_DELETE = "billing.invoice.delete"
    INVOICE_VOID = "billing.invoice.void"
    PAYMENT_VIEW = "billing.payment.view"
    PAYMENT_CREATE = "billing.payment.create"
    PAYMENT_REFUND = "billing.payment.refund"
    CLAIM_VIEW = "billing.claim.view"
    CLAIM_CREATE = "billing.claim.create"
    CLAIM_UPDATE = "billing.claim.update"
    CLAIM_APPROVE = "billing.claim.approve"
    CLAIM_REJECT = "billing.claim.reject"
    CLAIM_APPEAL = "billing.claim.appeal"
    CLAIM_SETTLE = "billing.claim.settle"


__all__ = ["BillingPermission"]
