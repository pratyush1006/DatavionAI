"""
Tax Filing model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.tax_gst.models.tax_rate import TaxRate
from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class TaxFiling(BaseModel):
    """
    Represents a tax filing within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="tax_gst_tax_filings",
    )

    tax_rate = models.ForeignKey(
        TaxRate,
        on_delete=models.PROTECT,
        related_name="tax_filings",
    )

    period = models.CharField(
        max_length=120,
        blank=True,
        help_text="Period.",
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
    reference = models.TextField(
        blank=True,
        help_text="Reference.",
    )
    taxable_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Taxable Amount.",
    )
    tax_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Tax Amount.",
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        help_text="Status.",
    )

    class Meta:
        db_table = "tax_gst_tax_filings"

        verbose_name = "Tax Filing"

        verbose_name_plural = "Tax Filings"

        ordering = ("-period_end",)

    def __str__(
        self,
    ) -> str:
        return f"{self.period or str(self.pk)}"


__all__ = [
    "TaxFiling",
]
