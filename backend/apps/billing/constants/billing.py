"""
Billing Core constants and lifecycle definitions.
"""

from __future__ import annotations

from django.db import models


class InvoiceStatus(models.TextChoices):
    """Invoice lifecycle states."""

    DRAFT = "DRAFT", "Draft"
    PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"
    PAID = "PAID", "Paid"
    OVERDUE = "OVERDUE", "Overdue"
    VOID = "VOID", "Void"


class PaymentMethod(models.TextChoices):
    """Supported payment methods."""

    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"
    UPI = "UPI", "UPI"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CHEQUE = "CHEQUE", "Cheque"
    INSURANCE = "INSURANCE", "Insurance"
    OTHER = "OTHER", "Other"


class ClaimStatus(models.TextChoices):
    """Insurance claim lifecycle states."""

    SUBMITTED = "SUBMITTED", "Submitted"
    APPROVED = "APPROVED", "Approved"
    PARTIALLY_APPROVED = "PARTIALLY_APPROVED", "Partially Approved"
    REJECTED = "REJECTED", "Rejected"
    APPEALED = "APPEALED", "Appealed"
    SETTLED = "SETTLED", "Settled"


DEFAULT_INVOICE_STATUS = InvoiceStatus.DRAFT


__all__ = (
    "ClaimStatus",
    "DEFAULT_INVOICE_STATUS",
    "InvoiceStatus",
    "PaymentMethod",
)
