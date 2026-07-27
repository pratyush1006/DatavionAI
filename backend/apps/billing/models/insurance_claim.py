"""
InsuranceClaim model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.constants import ClaimStatus
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class InsuranceClaim(BaseModel):
    """
    Represents an insurance claim submitted for an invoice.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="insurance_claims",
        help_text="Organization that submitted the claim.",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="insurance_claims",
        help_text="Patient associated with the claim.",
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.CASCADE,
        related_name="insurance_claims",
        help_text="Invoice the claim is for.",
    )

    insurance_provider = models.CharField(
        max_length=255,
        help_text="Name of the insurance provider.",
    )

    policy_number = models.CharField(
        max_length=100,
        help_text="Patient insurance policy number.",
    )

    claim_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique claim reference number.",
    )

    claim_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount claimed from insurance.",
    )

    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount approved by the insurer.",
    )

    status = models.CharField(
        max_length=20,
        choices=ClaimStatus.choices,
        default=ClaimStatus.SUBMITTED,
        db_index=True,
        help_text="Current status of the claim.",
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the claim was submitted.",
    )

    settled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the claim was settled.",
    )

    rejection_reason = models.TextField(
        blank=True,
        help_text="Reason for claim rejection, if applicable.",
    )

    class Meta:
        db_table = "billing_insurance_claims"

        verbose_name = "Insurance Claim"

        verbose_name_plural = "Insurance Claims"

        ordering = (
            "-submitted_at",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="billing_claim_org_status_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="billing_claim_pat_status_idx",
            ),
            models.Index(
                fields=[
                    "invoice",
                    "status",
                ],
                name="claim_invoice_status_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the claim display string.
        """

        return f"{self.claim_number} - {self.insurance_provider}"

    @property
    def is_approved(self) -> bool:
        """
        Return True if the claim is approved.
        """

        return self.status in (
            ClaimStatus.APPROVED,
            ClaimStatus.PARTIALLY_APPROVED,
            ClaimStatus.SETTLED,
        )

    @property
    def is_rejected(self) -> bool:
        """
        Return True if the claim is rejected.
        """

        return self.status == ClaimStatus.REJECTED

    @property
    def is_settled(self) -> bool:
        """
        Return True if the claim is settled.
        """

        return self.status == ClaimStatus.SETTLED


__all__ = [
    "InsuranceClaim",
]
