"""
Invoice model.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.billing.constants import (
    DEFAULT_INVOICE_STATUS,
    InvoiceStatus,
)
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Invoice(BaseModel):
    """
    Represents a billing invoice for a patient.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="invoices",
        help_text="Organization that owns the invoice.",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="invoices",
        help_text="Patient associated with the invoice.",
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique invoice number.",
    )

    invoice_date = models.DateField(
        help_text="Date the invoice was issued.",
    )

    due_date = models.DateField(
        help_text="Payment due date for the invoice.",
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total invoice amount.",
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total amount paid against the invoice.",
    )

    balance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Outstanding balance on the invoice.",
    )

    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=DEFAULT_INVOICE_STATUS,
        db_index=True,
        help_text="Current status of the invoice.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes for the invoice.",
    )

    class Meta:
        db_table = "invoices"

        verbose_name = "Invoice"

        verbose_name_plural = "Invoices"

        ordering = (
            "-invoice_date",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="invoice_org_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "invoice_date",
                ],
                name="invoice_org_date_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="invoice_patient_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the invoice display string.
        """

        return f"{self.invoice_number} - {self.patient}"

    @property
    def is_paid(self) -> bool:
        """
        Return True if the invoice is fully paid.
        """

        return self.status == InvoiceStatus.PAID

    @property
    def is_overdue(self) -> bool:
        """
        Return True if the invoice is overdue.
        """

        from django.utils import timezone

        return (
            self.balance_amount > Decimal("0.00")
            and self.due_date < timezone.now().date()
        )

    def update_status(self) -> None:
        """
        Update the invoice status based on payment amounts.
        """

        if self.paid_amount == Decimal("0.00"):
            self.status = InvoiceStatus.DRAFT
        elif self.paid_amount >= self.total_amount:
            self.status = InvoiceStatus.PAID
        elif self.paid_amount > Decimal("0.00"):
            self.status = InvoiceStatus.PARTIALLY_PAID
        elif self.is_overdue:
            self.status = InvoiceStatus.OVERDUE


__all__ = [
    "Invoice",
]
