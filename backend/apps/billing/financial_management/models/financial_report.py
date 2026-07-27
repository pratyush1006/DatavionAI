"""
Financial Report model.
"""

from __future__ import annotations

from apps.billing.financial_management.models import Budget
from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization
from django.db import models


class FinancialReport(BaseModel):
    """
    Represents a financial report within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="financial_management_financial_reports",
    )

    budget = models.ForeignKey(
        Budget,
        on_delete=models.PROTECT,
        related_name="financial_reports",
    )

    title = models.CharField(
        max_length=150,
        blank=True,
        help_text="Title.",
    )
    report_type = models.CharField(
        max_length=40,
        blank=True,
        help_text="Report Type.",
    )
    period_start = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Period Start.",
    )
    period_end = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Period End.",
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        help_text="Status.",
    )
    generated_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Generated At.",
    )

    class Meta:
        db_table = "financial_management_financial_reports"

        verbose_name = "Financial Report"

        verbose_name_plural = "Financial Reports"

        ordering = ("-period_end",)

    def __str__(
        self,
    ) -> str:
        return f"{self.title or str(self.pk)}"


__all__ = [
    "FinancialReport",
]
