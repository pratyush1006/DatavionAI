"""
Customer model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Customer(BaseModel):
    """
    Represents a customer within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="accounts_receivable_customers",
        help_text="Organization that owns the customer record.",
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
    email = models.CharField(
        max_length=120,
        blank=True,
        help_text="Email.",
    )
    phone = models.CharField(
        max_length=60,
        blank=True,
        help_text="Phone.",
    )
    address = models.TextField(
        blank=True,
        help_text="Address.",
    )
    tax_id = models.CharField(
        max_length=60,
        blank=True,
        help_text="Tax Id.",
    )
    credit_limit = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Credit Limit.",
    )

    class Meta:
        db_table = "accounts_receivable_customers"

        verbose_name = "Customer"

        verbose_name_plural = "Customers"

        ordering = ("name",)

    def __str__(
        self,
    ) -> str:
        return f"{self.name or str(self.pk)}"


__all__ = [
    "Customer",
]
