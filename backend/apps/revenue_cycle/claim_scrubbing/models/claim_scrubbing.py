"""
Claim Scrubbing models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Claim
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import ScrubResult


class ClaimScrubResult(BaseModel):
    """
    Result of scrubbing a claim before submission.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="claim_scrub_results",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="claim_scrub_results",
    )

    claim = models.OneToOneField(
        Claim,
        on_delete=models.CASCADE,
        related_name="scrub_result",
    )

    result = models.CharField(
        max_length=20,
        choices=ScrubResult.choices,
        default=ScrubResult.PASSED,
        db_index=True,
    )

    scrubbed_at = models.DateTimeField(
        auto_now_add=True,
    )

    scrubbed_by = models.CharField(
        max_length=150,
        blank=True,
    )

    errors = models.JSONField(
        default=list,
        blank=True,
        help_text="List of validation errors found.",
    )

    warnings = models.JSONField(
        default=list,
        blank=True,
        help_text="List of warnings found.",
    )

    class Meta:
        db_table = "claim_scrub_results"

        verbose_name = "Claim Scrub Result"

        verbose_name_plural = "Claim Scrub Results"

        ordering = ("-scrubbed_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "claim",
                    "result",
                ],
                name="scrub_org_claim_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Scrub {self.claim} ({self.get_result_display()})"


__all__ = [
    "ClaimScrubResult",
]
