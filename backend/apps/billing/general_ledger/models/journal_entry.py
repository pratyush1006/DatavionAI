"""
General Ledger journal entry model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.general_ledger.constants import EntryType
from apps.billing.general_ledger.models import GeneralLedgerAccount
from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class GeneralLedgerJournalEntry(BaseModel):
    """
    Represents a debit or credit journal entry against a ledger account.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="general_ledger_journal_entries",
    )

    account = models.ForeignKey(
        GeneralLedgerAccount,
        on_delete=models.PROTECT,
        related_name="journal_entries",
    )

    reference = models.CharField(
        max_length=60,
        help_text="External or internal reference number.",
    )

    entry_type = models.CharField(
        max_length=10,
        choices=EntryType.choices,
        help_text="Debit or credit entry.",
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        help_text="Entry amount.",
    )

    description = models.TextField(
        blank=True,
        help_text="Entry description.",
    )

    posted_at = models.DateTimeField(
        db_index=True,
        help_text="When the entry was posted.",
    )

    class Meta:
        db_table = "general_ledger_journal_entries"

        verbose_name = "General Ledger Journal Entry"

        verbose_name_plural = "General Ledger Journal Entries"

        ordering = ("-posted_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "account",
                    "posted_at",
                ],
                name="gl_entry_org_acct_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.reference} - {self.entry_type} {self.amount}"


__all__ = [
    "GeneralLedgerJournalEntry",
]
