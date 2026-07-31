"""
Charge Capture models.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class ChargeCapture(BaseModel):
    """
    A captured charge for services rendered, pending coding and billing.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="charge_captures",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="charge_captures",
    )

    encounter_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Source encounter / visit identifier.",
    )

    service_date = models.DateField(
        help_text="Date the service was rendered.",
    )

    description = models.CharField(
        max_length=255,
        help_text="Service description.",
    )

    procedure_code = models.CharField(
        max_length=30,
        blank=True,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    captured_by = models.CharField(
        max_length=150,
        blank=True,
    )

    is_coded = models.BooleanField(
        default=False,
        help_text="Whether coding has been completed.",
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "charge_captures"

        verbose_name = "Charge Capture"

        verbose_name_plural = "Charge Captures"

        ordering = ("-service_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "service_date",
                ],
                name="charge_org_pat_date_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Charge {self.description} ({self.total_charge})"


__all__ = [
    "ChargeCapture",
]
