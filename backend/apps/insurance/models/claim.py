"""
Insurance claim model.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.constants import (
    DEFAULT_CLAIM_STATUS,
    ClaimStatus,
)
from apps.insurance.models.enrollment import Enrollment
from apps.platform.organizations.models import Organization


class Claim(BaseModel):
    """
    Represents an insurance claim submitted for reimbursement.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="claims",
        help_text="Organization that owns the claim.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="claims",
        help_text="Patient associated with the claim.",
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="claims",
        help_text="Enrollment used for the claim.",
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claims",
        help_text="Invoice associated with the claim.",
    )

    claim_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique claim number.",
    )

    claim_date = models.DateField(
        help_text="Date the claim was created.",
    )

    diagnosis_codes = models.JSONField(
        default=list,
        blank=True,
        help_text="List of diagnosis codes (ICD).",
    )

    procedure_codes = models.JSONField(
        default=list,
        blank=True,
        help_text="List of procedure codes (CPT/HCPCS).",
    )

    charged_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount charged for the claim.",
    )

    allowed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount allowed by the insurer.",
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount paid by the insurer.",
    )

    status = models.CharField(
        max_length=20,
        choices=ClaimStatus.choices,
        default=DEFAULT_CLAIM_STATUS,
        help_text="Claim lifecycle status.",
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the claim was submitted.",
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the claim was paid.",
    )

    denial_reason = models.TextField(
        blank=True,
        help_text="Reason provided when the claim is denied.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the claim was created.",
    )

    class Meta:
        db_table = "insurance_claims"

        verbose_name = "Claim"

        verbose_name_plural = "Claims"

        ordering = (
            "patient",
            "claim_date",
        )

        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="claim_patient_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="claim_org_status_idx",
            ),
            models.Index(
                fields=[
                    "enrollment",
                    "claim_date",
                ],
                name="claim_enrollment_date_idx",
            ),
        ]

    @property
    def outstanding_amount(self) -> Decimal:
        """
        Return the amount still owed on the claim.
        """

        allowed = self.allowed_amount or Decimal("0.00")
        paid = self.paid_amount or Decimal("0.00")

        return max(
            allowed - paid,
            Decimal("0.00"),
        )

    def __str__(self) -> str:
        """
        Return the claim display name.
        """

        return f"{self.claim_number} ({self.status})"


__all__ = [
    "Claim",
]
