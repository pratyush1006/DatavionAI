"""
Budget model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Budget(BaseModel):
    """
    Represents a budget within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="financial_management_budgets",
        help_text="Organization that owns the budget record.",
    )

    name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name.",
    )
    fiscal_year = models.CharField(
        max_length=60,
        blank=True,
        help_text="Fiscal Year.",
    )
    total_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total Amount.",
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        help_text="Status.",
    )

    class Meta:
        db_table = "financial_management_budgets"

        verbose_name = "Budget"

        verbose_name_plural = "Budgets"

        ordering = (
            "fiscal_year",
            "name",
        )

    def __str__(
        self,
    ) -> str:
        return f"{self.name or str(self.pk)}"


__all__ = [
    "Budget",
]
