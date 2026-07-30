"""
Billing models.
"""

from __future__ import annotations

from decimal import Decimal

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import BatchStatus
from django.db import models


class BillingBatch(BaseModel):
    """
    A batch of charges / claims grouped for billing cycle processing.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="billing_batches",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="billing_batches",
        null=True,
        blank=True,
        help_text="Patient for patient-level batches; blank for org batches.",
    )

    batch_number = models.CharField(
        max_length=50,
        help_text="Unique billing batch identifier.",
    )

    status = models.CharField(
        max_length=20,
        choices=BatchStatus.choices,
        default=BatchStatus.OPEN,
        db_index=True,
    )

    billing_period_start = models.DateField(
        null=True,
        blank=True,
    )

    billing_period_end = models.DateField(
        null=True,
        blank=True,
    )

    item_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of items in the batch.",
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_by = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "billing_batches"

        verbose_name = "Billing Batch"

        verbose_name_plural = "Billing Batches"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="batch_org_status_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "batch_number",
                ],
                name="unique_billing_batch_number",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Batch {self.batch_number} ({self.get_status_display()})"


__all__ = [
    "BillingBatch",
]
