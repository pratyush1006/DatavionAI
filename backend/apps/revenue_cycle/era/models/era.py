"""
ERA (Electronic Remittance Advice) models.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.billing.models.payment import Payment
from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Claim
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import RemittanceType


class RemittanceAdvice(BaseModel):
    """
    Electronic remittance advice (ERA) describing payer payment / adjustments.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="remittance_advices",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="remittance_advices",
    )

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name="remittance_advices",
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="remittance_advices",
    )

    remittance_type = models.CharField(
        max_length=20,
        choices=RemittanceType.choices,
        default=RemittanceType.PAYMENT,
    )

    payer_name = models.CharField(
        max_length=200,
        blank=True,
    )

    payer_claim_control_number = models.CharField(
        max_length=100,
        blank=True,
    )

    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    patient_responsibility = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    adjustment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    remittance_date = models.DateField(
        help_text="Date of the remittance advice.",
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    raw_content = models.TextField(
        blank=True,
        help_text="Raw X12 835 content, if stored.",
    )

    class Meta:
        db_table = "remittance_advices"

        verbose_name = "Remittance Advice"

        verbose_name_plural = "Remittance Advices"

        ordering = ("-remittance_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "claim",
                    "remittance_type",
                ],
                name="era_org_claim_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"ERA {self.claim} ({self.payment_amount})"


__all__ = [
    "RemittanceAdvice",
]
