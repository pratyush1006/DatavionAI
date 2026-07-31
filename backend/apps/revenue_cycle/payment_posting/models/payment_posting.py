"""
Payment Posting models.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.billing.models.invoice import Invoice
from apps.billing.models.payment import Payment
from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import PostingStatus


class PaymentPosting(BaseModel):
    """
    Allocation of a payment against an invoice / charge.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payment_postings",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="payment_postings",
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="postings",
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payment_postings",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Amount posted to the invoice.",
    )

    posting_date = models.DateField(
        help_text="Date the payment was posted.",
    )

    status = models.CharField(
        max_length=20,
        choices=PostingStatus.choices,
        default=PostingStatus.POSTED,
        db_index=True,
    )

    posted_by = models.CharField(
        max_length=150,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "payment_postings"

        verbose_name = "Payment Posting"

        verbose_name_plural = "Payment Postings"

        ordering = ("-posting_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "payment",
                    "invoice",
                ],
                name="post_org_pay_inv_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Posting {self.payment} -> {self.invoice}"


__all__ = [
    "PaymentPosting",
]
