"""Shared Billing lifecycle statuses."""

from __future__ import annotations

from django.db import models


class FinancialDocumentStatus(models.TextChoices):
    """Generic financial document lifecycle."""

    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    VOID = "void", "Void"
    CANCELLED = "cancelled", "Cancelled"


class FinancialTransactionStatus(models.TextChoices):
    """Generic financial transaction lifecycle."""

    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REVERSED = "reversed", "Reversed"
    REFUNDED = "refunded", "Refunded"


class ClaimStatus(models.TextChoices):
    """Healthcare insurance claim lifecycle."""

    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    APPEALED = "appealed", "Appealed"
    SETTLED = "settled", "Settled"


__all__ = ["ClaimStatus", "FinancialDocumentStatus", "FinancialTransactionStatus"]
