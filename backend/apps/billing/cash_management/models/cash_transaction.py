"""
Cash Transaction model.
"""

from __future__ import annotations

from apps.billing.cash_management.models import BankAccount
from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization
from django.db import models


class CashTransaction(BaseModel):
    """
    Represents a cash transaction within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="cash_management_cash_transactions",
    )

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
        related_name="cash_transactions",
    )

    reference = models.TextField(
        blank=True,
        help_text="Reference.",
    )
    transaction_type = models.CharField(
        max_length=40,
        blank=True,
        help_text="Transaction Type.",
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount.",
    )
    description = models.TextField(
        blank=True,
        help_text="Description.",
    )
    transaction_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Transaction Date.",
    )

    class Meta:
        db_table = "cash_management_cash_transactions"

        verbose_name = "Cash Transaction"

        verbose_name_plural = "Cash Transactions"

        ordering = ("-transaction_date",)

    def __str__(
        self,
    ) -> str:
        return f"{self.reference or str(self.pk)}"


__all__ = [
    "CashTransaction",
]
