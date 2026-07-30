"""
Vendor model.
"""

from __future__ import annotations

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from django.db import models


class Vendor(BaseModel):
    """
    Represents a vendor within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="accounts_payable_vendors",
        help_text="Organization that owns the vendor record.",
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

    class Meta:
        db_table = "accounts_payable_vendors"

        verbose_name = "Vendor"

        verbose_name_plural = "Vendors"

        ordering = ("name",)

    def __str__(
        self,
    ) -> str:
        return f"{self.name or str(self.pk)}"


__all__ = [
    "Vendor",
]
