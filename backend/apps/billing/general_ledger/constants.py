"""
General Ledger-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class AccountType(models.TextChoices):
    """
    General ledger account types.
    """

    ASSET = "asset", "Asset"
    LIABILITY = "liability", "Liability"
    EQUITY = "equity", "Equity"
    REVENUE = "revenue", "Revenue"
    EXPENSE = "expense", "Expense"


class AccountStatus(models.TextChoices):
    """
    Lifecycle status of a general ledger account.
    """

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    CLOSED = "closed", "Closed"
    ARCHIVED = "archived", "Archived"


class EntryType(models.TextChoices):
    """
    Journal entry type.
    """

    DEBIT = "debit", "Debit"
    CREDIT = "credit", "Credit"


DEFAULT_ACCOUNT_STATUS: Final[str] = AccountStatus.ACTIVE


__all__ = [
    "AccountStatus",
    "AccountType",
    "DEFAULT_ACCOUNT_STATUS",
    "EntryType",
]
