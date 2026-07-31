"""
Accounts Receivable models.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.billing.models.invoice import Invoice
from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import ArStatus


class AccountsReceivable(BaseModel):
    """
    An accounts-receivable record tracking outstanding patient balances.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="accounts_receivables",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="accounts_receivables",
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="ar_records",
    )

    billed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    adjustment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=20,
        choices=ArStatus.choices,
        default=ArStatus.CURRENT,
        db_index=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    last_activity_date = models.DateField(
        null=True,
        blank=True,
    )

    assigned_to = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "accounts_receivables"

        verbose_name = "Accounts Receivable"

        verbose_name_plural = "Accounts Receivables"

        ordering = (
            "status",
            "due_date",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="ar_org_pat_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"AR {self.invoice} ({self.get_status_display()})"


__all__ = [
    "AccountsReceivable",
]
