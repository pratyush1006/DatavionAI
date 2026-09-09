"""Constants and lifecycle definitions for Accounts Receivable."""

from __future__ import annotations

from django.db import models


class ARAccountStatus(models.TextChoices):
    """Supported Accounts Receivable account states."""

    OPEN = "OPEN", "Open"
    ON_HOLD = "ON_HOLD", "On Hold"
    PAID = "PAID", "Paid"
    WRITTEN_OFF = "WRITTEN_OFF", "Written Off"
    CLOSED = "CLOSED", "Closed"


class ARTransactionType(models.TextChoices):
    """Supported Accounts Receivable transaction types."""

    CHARGE = "CHARGE", "Charge"
    PAYMENT = "PAYMENT", "Payment"
    ADJUSTMENT = "ADJUSTMENT", "Adjustment"
    DENIAL = "DENIAL", "Denial"
    WRITE_OFF = "WRITE_OFF", "Write Off"
    REFUND = "REFUND", "Refund"


class ARTransactionStatus(models.TextChoices):
    """Supported Accounts Receivable transaction states."""

    POSTED = "POSTED", "Posted"
    REVERSED = "REVERSED", "Reversed"


class ARHoldReason(models.TextChoices):
    """Supported account hold reasons."""

    MANUAL_REVIEW = "MANUAL_REVIEW", "Manual Review"
    DISPUTE = "DISPUTE", "Dispute"
    INSURANCE = "INSURANCE", "Insurance"
    COLLECTIONS = "COLLECTIONS", "Collections"


class ARAction(models.TextChoices):
    """Auditable Accounts Receivable actions."""

    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    POST = "POST", "Post"
    REVERSE = "REVERSE", "Reverse"
    HOLD = "HOLD", "Hold"
    RELEASE_HOLD = "RELEASE_HOLD", "Release Hold"
    WRITE_OFF = "WRITE_OFF", "Write Off"
    CLOSE = "CLOSE", "Close"
    RESTORE = "RESTORE", "Restore"


__all__ = (
    "ARAccountStatus",
    "ARAction",
    "ARHoldReason",
    "ARTransactionStatus",
    "ARTransactionType",
)
