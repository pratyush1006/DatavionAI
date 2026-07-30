"""
Claim Submission models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Claim
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import (
    ClaimPriority,
    SubmissionMethod,
)


class ClaimSubmission(BaseModel):
    """
    Record of a claim submission to a payer or clearinghouse.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="claim_submissions",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="claim_submissions",
    )

    claim = models.OneToOneField(
        Claim,
        on_delete=models.CASCADE,
        related_name="submission",
    )

    submission_method = models.CharField(
        max_length=20,
        choices=SubmissionMethod.choices,
        default=SubmissionMethod.ELECTRONIC,
    )

    priority = models.CharField(
        max_length=20,
        choices=ClaimPriority.choices,
        default=ClaimPriority.NORMAL,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    submitted_by = models.CharField(
        max_length=150,
        blank=True,
    )

    clearinghouse = models.CharField(
        max_length=150,
        blank=True,
    )

    acknowledgement_code = models.CharField(
        max_length=50,
        blank=True,
    )

    payer_control_number = models.CharField(
        max_length=100,
        blank=True,
    )

    transmission_status = models.CharField(
        max_length=50,
        blank=True,
        help_text="Status returned by the clearinghouse.",
    )

    class Meta:
        db_table = "claim_submissions"

        verbose_name = "Claim Submission"

        verbose_name_plural = "Claim Submissions"

        ordering = (
            "-submitted_at",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "claim",
                ],
                name="sub_org_claim_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Submission {self.claim}"


__all__ = [
    "ClaimSubmission",
]
