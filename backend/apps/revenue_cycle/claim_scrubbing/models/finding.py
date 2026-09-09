"""Claim scrub finding model."""

from __future__ import annotations

from django.db import models

from apps.core.models.base import BaseModel
from apps.revenue_cycle.claim_scrubbing.constants import FindingSeverity


class ClaimScrubFinding(BaseModel):
    """Record a deterministic rule violation discovered during scrubbing."""

    scrub = models.ForeignKey(
        "revenue_cycle.ClaimScrub",
        on_delete=models.CASCADE,
        related_name="findings",
    )
    rule = models.ForeignKey(
        "revenue_cycle.ScrubRule",
        on_delete=models.PROTECT,
        related_name="findings",
    )
    field_name = models.CharField(max_length=120)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=FindingSeverity.choices)
    is_blocking = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    observed_value = models.JSONField(null=True, blank=True)

    class Meta:
        """Define indexes for finding review."""

        db_table = "revenue_cycle_claim_scrub_findings"
        indexes = (
            models.Index(
                fields=("scrub", "is_blocking", "is_resolved"),
                name="rc_scrub_find_block_idx",
            ),
        )


__all__ = ("ClaimScrubFinding",)
