"""
Permission classes for the Payment Posting module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PaymentPostingPermission:
    VIEW = "payment_posting.view"
    CREATE = "payment_posting.create"
    UPDATE = "payment_posting.update"
    DELETE = "payment_posting.delete"


class CanViewPaymentPosting(BasePermission):
    permission_code = PaymentPostingPermission.VIEW


class CanCreatePaymentPosting(BasePermission):
    permission_code = PaymentPostingPermission.CREATE


class CanUpdatePaymentPosting(BasePermission):
    permission_code = PaymentPostingPermission.UPDATE


class CanDeletePaymentPosting(BasePermission):
    permission_code = PaymentPostingPermission.DELETE


__all__ = [
    "CanCreatePaymentPosting",
    "CanDeletePaymentPosting",
    "CanUpdatePaymentPosting",
    "CanViewPaymentPosting",
    "PaymentPostingPermission",
]
