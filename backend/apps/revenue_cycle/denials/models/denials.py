"""
Denials models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Claim
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import DenialReason


class ClaimDenial(BaseModel):
    """
    A denied or rejected claim requiring follow-up.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="claim_denials",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="claim_denials",
    )

    claim = models.OneToOneField(
        Claim,
        on_delete=models.CASCADE,
        related_name="denial",
    )

    denial_reason = models.CharField(
        max_length=20,
        choices=DenialReason.choices,
        default=DenialReason.OTHER,
    )

    payer_reason_code = models.CharField(
        max_length=50,
        blank=True,
    )

    denial_date = models.DateField(
        help_text="Date the denial was received.",
    )

    description = models.TextField(
        blank=True,
    )

    is_appealable = models.BooleanField(
        default=True,
    )

    resolved = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "claim_denials"

        verbose_name = "Claim Denial"

        verbose_name_plural = "Claim Denials"

        ordering = ("-denial_date",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "claim",
                    "resolved",
                ],
                name="denial_org_claim_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Denial {self.claim} ({self.get_denial_reason_display()})"


__all__ = [
    "ClaimDenial",
]
