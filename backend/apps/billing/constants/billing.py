"""
Billing-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class InvoiceStatus(models.TextChoices):
    """
    Invoice lifecycle status.
    """

    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    VOID = "void", "Void"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethod(models.TextChoices):
    """
    Supported payment methods.
    """

    CASH = "cash", "Cash"
    CARD = "card", "Card"
    UPI = "upi", "UPI"
    NET_BANKING = "net_banking", "Net Banking"
    INSURANCE = "insurance", "Insurance"
    CHEQUE = "cheque", "Cheque"
    OTHER = "other", "Other"


class ClaimStatus(models.TextChoices):
    """
    Insurance claim lifecycle status.
    """

    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under Review"
    APPROVED = "approved", "Approved"
    PARTIALLY_APPROVED = "partially_approved", "Partially Approved"
    REJECTED = "rejected", "Rejected"
    APPEALED = "appealed", "Appealed"
    SETTLED = "settled", "Settled"


DEFAULT_INVOICE_STATUS: Final[str] = InvoiceStatus.DRAFT


__all__ = [
    "DEFAULT_INVOICE_STATUS",
    "ClaimStatus",
    "InvoiceStatus",
    "PaymentMethod",
]
