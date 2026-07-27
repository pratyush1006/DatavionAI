"""
InvoiceItem model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class InvoiceItem(BaseModel):
    """
    Represents a line item on an invoice.
    """

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Invoice this item belongs to.",
    )

    description = models.CharField(
        max_length=255,
        help_text="Description of the service or item.",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of the item.",
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per unit.",
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total price for this line item.",
    )

    service_code = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional service or CPT code.",
    )

    class Meta:
        db_table = "invoice_items"

        verbose_name = "Invoice Item"

        verbose_name_plural = "Invoice Items"

        indexes = [
            models.Index(
                fields=[
                    "invoice",
                    "service_code",
                ],
                name="invoice_item_code_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the invoice item display string.
        """

        return f"{self.description} ({self.invoice.invoice_number})"

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Calculate total_price from quantity and unit_price.
        """

        self.total_price = self.quantity * self.unit_price

        super().save(
            *args,
            **kwargs,
        )


__all__ = [
    "InvoiceItem",
]
