from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization

from .fiscal_period import FiscalPeriod
from .ledger_account import LedgerAccount


class JournalEntry(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="finance_journal_entries"
    )
    fiscal_period = models.ForeignKey(
        FiscalPeriod, on_delete=models.PROTECT, related_name="journal_entries"
    )
    reference = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    entry_date = models.DateField()
    status = models.CharField(max_length=20, default="draft")
    total_debit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    posted_at = models.DateTimeField(null=True, blank=True)
    reversal_of = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="reversal_entry",
    )

    class Meta:
        db_table = "finance_journal_entries"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "reference"),
                name="finance_journal_org_reference_uniq",
            )
        ]

    def clean(self):
        if self.total_debit < Decimal("0") or self.total_credit < Decimal("0"):
            raise ValidationError("Journal totals cannot be negative.")


class JournalLine(BaseModel):
    entry = models.ForeignKey(
        JournalEntry, on_delete=models.CASCADE, related_name="lines"
    )
    account = models.ForeignKey(
        LedgerAccount, on_delete=models.PROTECT, related_name="journal_lines"
    )
    description = models.TextField(blank=True)
    debit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "finance_journal_lines"

    def clean(self):
        if self.debit < Decimal("0") or self.credit < Decimal("0"):
            raise ValidationError("Journal line values cannot be negative.")
        if self.debit == Decimal("0") and self.credit == Decimal("0"):
            raise ValidationError("A journal line must contain a debit or credit.")
        if self.debit > Decimal("0") and self.credit > Decimal("0"):
            raise ValidationError(
                "A journal line cannot contain both debit and credit."
            )
