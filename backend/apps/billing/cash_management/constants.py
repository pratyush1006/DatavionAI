"""
Cash Management-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class TransactionType(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"
    TRANSFER = "transfer", "Transfer"
    FEE = "fee", "Fee"
    INTEREST = "interest", "Interest"


DEFAULT_CURRENCY: Final[str] = "INR"


__all__ = [
    "TransactionType",
]
