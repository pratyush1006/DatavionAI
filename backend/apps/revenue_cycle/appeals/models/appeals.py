"""
Appeals models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Claim
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import AppealStatus
from apps.revenue_cycle.denials.models import ClaimDenial


class ClaimAppeal(BaseModel):
    """
    An appeal filed against a denied claim.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="claim_appeals",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="claim_appeals",
    )

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name="appeals",
    )

    denial = models.ForeignKey(
        ClaimDenial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appeals",
    )

    status = models.CharField(
        max_length=20,
        choices=AppealStatus.choices,
        default=AppealStatus.DRAFT,
        db_index=True,
    )

    appeal_reason = models.TextField(
        help_text="Reason for the appeal.",
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    decided_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    decision_notes = models.TextField(
        blank=True,
    )

    filed_by = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "claim_appeals"

        verbose_name = "Claim Appeal"

        verbose_name_plural = "Claim Appeals"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "claim",
                    "status",
                ],
                name="appeal_org_claim_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Appeal {self.claim} ({self.get_status_display()})"


__all__ = [
    "ClaimAppeal",
]
