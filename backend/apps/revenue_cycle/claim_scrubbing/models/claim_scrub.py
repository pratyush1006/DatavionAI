"""Claim scrub aggregate model."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_scrubbing.constants import ScrubStatus


class ClaimScrub(BaseModel):
    """Represent one deterministic scrub execution for a claim reference."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="revenue_cycle_claim_scrubs",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_claim_scrubs",
    )
    claim_reference = models.CharField(max_length=120)
    idempotency_key = models.CharField(max_length=160)
    status = models.CharField(
        max_length=20,
        choices=ScrubStatus.choices,
        default=ScrubStatus.PENDING,
        db_index=True,
    )
    input_snapshot = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    override_reason = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_claim_scrubs",
    )

    class Meta:
        """Define tenant-safe uniqueness and query indexes."""

        db_table = "revenue_cycle_claim_scrubs"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_claim_scrub_org_idempotency_uniq",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "claim_reference", "status"),
                name="rc_claim_scrub_org_claim_idx",
            ),
            models.Index(
                fields=("organization", "patient", "created_at"),
                name="rc_claim_scrub_org_patient_idx",
            ),
        )

    @property
    def has_blocking_findings(self) -> bool:
        """Return whether this scrub contains blocking findings."""

        return self.findings.filter(is_blocking=True, is_resolved=False).exists()


__all__ = ("ClaimScrub",)
