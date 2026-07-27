"""
Accounts Payable-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    CANCELLED = "cancelled", "Cancelled"


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    APPROVED = "approved", "Approved"
    PAID = "paid", "Paid"
    VOID = "void", "Void"


DEFAULT_VENDOR_STATUS: Final[str] = "active"


__all__ = [
    "InvoiceStatus",
    "PaymentStatus",
]
