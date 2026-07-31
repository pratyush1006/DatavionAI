"""
Tax Rate model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class TaxRate(BaseModel):
    """
    Represents a tax rate within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="tax_gst_tax_rates",
        help_text="Organization that owns the tax_rate record.",
    )

    code = models.CharField(
        max_length=60,
        blank=True,
        help_text="Code.",
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name.",
    )
    rate = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Rate.",
    )
    tax_type = models.CharField(
        max_length=40,
        blank=True,
        help_text="Tax Type.",
    )
    description = models.TextField(
        blank=True,
        help_text="Description.",
    )

    class Meta:
        db_table = "tax_gst_tax_rates"

        verbose_name = "Tax Rate"

        verbose_name_plural = "Tax Rates"

        ordering = ("name",)

    def __str__(
        self,
    ) -> str:
        return f"{self.name or str(self.pk)}"


__all__ = [
    "TaxRate",
]
