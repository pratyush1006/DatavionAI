"""
Bank Account model.
"""

from __future__ import annotations

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from django.db import models


class BankAccount(BaseModel):
    """
    Represents a bank account within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="cash_management_bank_accounts",
        help_text="Organization that owns the bank_account record.",
    )

    name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name.",
    )
    bank_name = models.CharField(
        max_length=60,
        blank=True,
        help_text="Bank Name.",
    )
    account_number = models.CharField(
        max_length=60,
        blank=True,
        help_text="Account Number.",
    )
    currency = models.CharField(
        max_length=40,
        blank=True,
        help_text="Currency.",
    )
    opening_balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Opening Balance.",
    )
    current_balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Current Balance.",
    )

    class Meta:
        db_table = "cash_management_bank_accounts"

        verbose_name = "Bank Account"

        verbose_name_plural = "Bank Accounts"

        ordering = ("name",)

    def __str__(
        self,
    ) -> str:
        return f"{self.name or str(self.pk)}"


__all__ = [
    "BankAccount",
]
