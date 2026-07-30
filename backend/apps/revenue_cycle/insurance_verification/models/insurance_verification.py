"""
Insurance Verification models.
"""

from __future__ import annotations

from decimal import Decimal

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Enrollment
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import VerificationStatus
from django.db import models


class InsuranceVerification(BaseModel):
    """
    Verification of a patient's insurance coverage with the payer.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="insurance_verifications",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="insurance_verifications",
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    verification_date = models.DateField(
        help_text="Date the verification was performed.",
    )

    status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    verified_by = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name of the person who verified coverage.",
    )

    member_id = models.CharField(
        max_length=100,
        blank=True,
    )

    plan_name = models.CharField(
        max_length=200,
        blank=True,
    )

    coverage_active = models.BooleanField(
        null=True,
        blank=True,
    )

    deductible_remaining = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal("0.00"),
    )

    copay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal("0.00"),
    )

    coinsurance_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal("0.00"),
    )

    notes = models.TextField(
        blank=True,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "insurance_verifications"

        verbose_name = "Insurance Verification"

        verbose_name_plural = "Insurance Verifications"

        ordering = ("-verification_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "status",
                ],
                name="verif_org_pat_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Verification {self.patient} ({self.get_status_display()})"


__all__ = [
    "InsuranceVerification",
]
