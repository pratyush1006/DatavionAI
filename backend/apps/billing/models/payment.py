"""
Payment model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.constants import PaymentMethod
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Payment(BaseModel):
    """
    Represents a payment received against an invoice.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Organization that received the payment.",
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Invoice the payment is applied to.",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Patient who made the payment.",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        help_text="Method used for the payment.",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Payment amount.",
    )

    payment_date = models.DateField(
        help_text="Date the payment was received.",
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional reference or transaction number.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional payment notes.",
    )

    received_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_payments",
        help_text="User who recorded the payment.",
    )

    class Meta:
        db_table = "payments"

        verbose_name = "Payment"

        verbose_name_plural = "Payments"

        ordering = (
            "-payment_date",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "payment_date",
                ],
                name="payment_org_date_idx",
            ),
            models.Index(
                fields=[
                    "invoice",
                    "payment_date",
                ],
                name="payment_invoice_date_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "payment_date",
                ],
                name="payment_patient_date_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the payment display string.
        """

        return f"{self.payment_method} - {self.amount} ({self.invoice.invoice_number})"

    @property
    def is_refunded(self) -> bool:
        """
        Return True if the payment has been refunded.
        """

        return self.refunds.filter(
            is_active=True,
        ).exists()


__all__ = [
    "Payment",
]
