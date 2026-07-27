"""
Billing permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class BillingPermission:
    """
    Billing permission codes.
    """

    VIEW = "billing.view"
    CREATE = "billing.create"
    UPDATE = "billing.update"
    DELETE = "billing.delete"
    VOID = "billing.void"
    PROCESS_PAYMENT = "billing.process_payment"
    SUBMIT_CLAIM = "billing.submit_claim"
    APPROVE_CLAIM = "billing.approve_claim"


class CanViewInvoice(BasePermission):
    """
    Permission required to view billing invoices.
    """

    permission_code = BillingPermission.VIEW


class CanCreateInvoice(BasePermission):
    """
    Permission required to create invoices.
    """

    permission_code = BillingPermission.CREATE


class CanUpdateInvoice(BasePermission):
    """
    Permission required to update invoices.
    """

    permission_code = BillingPermission.UPDATE


class CanDeleteInvoice(BasePermission):
    """
    Permission required to delete invoices.
    """

    permission_code = BillingPermission.DELETE


class CanVoidInvoice(BasePermission):
    """
    Permission required to void invoices.
    """

    permission_code = BillingPermission.VOID


class CanProcessPayment(BasePermission):
    """
    Permission required to process payments.
    """

    permission_code = BillingPermission.PROCESS_PAYMENT


class CanSubmitClaim(BasePermission):
    """
    Permission required to submit insurance claims.
    """

    permission_code = BillingPermission.SUBMIT_CLAIM


class CanApproveClaim(BasePermission):
    """
    Permission required to approve insurance claims.
    """

    permission_code = BillingPermission.APPROVE_CLAIM


__all__ = [
    "BillingPermission",
    "CanApproveClaim",
    "CanCreateInvoice",
    "CanDeleteInvoice",
    "CanProcessPayment",
    "CanSubmitClaim",
    "CanUpdateInvoice",
    "CanViewInvoice",
    "CanVoidInvoice",
]
