"""Persistent deterministic claim scrub rules."""

from __future__ import annotations

from django.db import models

from apps.core.models.base import BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_scrubbing.constants import RuleType


class ScrubRule(BaseModel):
    """Define a tenant-scoped rule used to validate claim data."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="revenue_cycle_scrub_rules",
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=160)
    rule_type = models.CharField(max_length=30, choices=RuleType.choices)
    field_name = models.CharField(max_length=120)
    configuration = models.JSONField(default=dict, blank=True)
    severity = models.CharField(max_length=20, default="error")
    is_blocking = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=100)

    class Meta:
        """Define database constraints and indexes."""

        db_table = "revenue_cycle_scrub_rules"
        ordering = ("priority", "code")
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="rc_scrub_rule_org_code_uniq",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "is_active", "priority"),
                name="rc_scrub_rule_org_active_idx",
            ),
        )


__all__ = ("ScrubRule",)
