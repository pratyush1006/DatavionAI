"""
Accounts Receivable-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    VOID = "void", "Void"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RECEIVED = "received", "Received"
    PARTIAL = "partial", "Partial"


DEFAULT_CUSTOMER_STATUS: Final[str] = "active"


__all__ = [
    "InvoiceStatus",
    "PaymentStatus",
]
