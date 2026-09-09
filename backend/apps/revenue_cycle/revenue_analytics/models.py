"""Persistent models for Revenue Cycle analytics snapshots."""

from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel

from .constants import AnalyticsPeriod


class RevenueMetricSnapshot(BaseModel):
    """Store an organization-scoped, reproducible revenue KPI snapshot."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_metric_snapshots",
    )
    period = models.CharField(
        max_length=10,
        choices=AnalyticsPeriod.choices,
    )
    period_start = models.DateField()
    period_end = models.DateField()
    gross_charges = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    payments = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    adjustments = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    denials = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    write_offs = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    outstanding_ar = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    encounter_count = models.PositiveBigIntegerField(default=0)
    claim_count = models.PositiveBigIntegerField(default=0)
    denied_claim_count = models.PositiveBigIntegerField(default=0)
    paid_claim_count = models.PositiveBigIntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Configure snapshot uniqueness and analytics indexes."""

        db_table = "revenue_cycle_metric_snapshots"
        ordering = ("-period_end", "-generated_at")
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "period",
                    "period_start",
                    "period_end",
                ),
                name="unique_rc_metric_snapshot_period",
            ),
            models.CheckConstraint(
                condition=Q(period_end__gte=models.F("period_start")),
                name="rc_metric_valid_period",
            ),
            models.CheckConstraint(
                condition=Q(gross_charges__gte=0),
                name="rc_metric_charges_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(payments__gte=0),
                name="rc_metric_payments_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(adjustments__gte=0),
                name="rc_metric_adjustments_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(denials__gte=0),
                name="rc_metric_denials_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(write_offs__gte=0),
                name="rc_metric_writeoffs_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(outstanding_ar__gte=0),
                name="rc_metric_ar_non_negative",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "period_end"),
                name="rc_metric_org_period_idx",
            ),
            models.Index(
                fields=("organization", "period"),
                name="rc_metric_org_type_idx",
            ),
        )

    def __str__(self) -> str:
        """Return the snapshot period."""

        return f"{self.period}:{self.period_start}:{self.period_end}"


__all__ = ("RevenueMetricSnapshot",)
