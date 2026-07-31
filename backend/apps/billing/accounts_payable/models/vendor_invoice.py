"""
Vendor Invoice model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.accounts_payable.models import Vendor
from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization


class VendorInvoice(BaseModel):
    """
    Represents a vendor invoice within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="accounts_payable_vendor_invoices",
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name="vendor_invoices",
    )

    invoice_number = models.CharField(
        max_length=60,
        blank=True,
        help_text="Invoice Number.",
    )
    reference = models.TextField(
        blank=True,
        help_text="Reference.",
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount.",
    )
    tax_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Tax Amount.",
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Due Date.",
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        help_text="Status.",
    )

    class Meta:
        db_table = "accounts_payable_vendor_invoices"

        verbose_name = "Vendor Invoice"

        verbose_name_plural = "Vendor Invoices"

        ordering = ("-due_date",)

    def __str__(
        self,
    ) -> str:
        return f"{self.invoice_number or str(self.pk)}"


__all__ = [
    "VendorInvoice",
]
