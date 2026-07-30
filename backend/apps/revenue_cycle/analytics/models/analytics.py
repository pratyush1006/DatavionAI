"""
Analytics models.
"""

from __future__ import annotations

from decimal import Decimal

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import MetricCategory
from django.db import models


class RcmMetric(BaseModel):
    """
    A stored RCM analytics metric (e.g. DSO, denial rate, collection rate).
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="rcm_metrics",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="rcm_metrics",
        null=True,
        blank=True,
    )

    category = models.CharField(
        max_length=20,
        choices=MetricCategory.choices,
        default=MetricCategory.REVENUE,
        db_index=True,
    )

    name = models.CharField(
        max_length=100,
        help_text="Metric name (e.g. days_sales_outstanding).",
    )

    value = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=Decimal("0.0000"),
    )

    unit = models.CharField(
        max_length=30,
        blank=True,
        help_text="Unit of measure (e.g. days, percent).",
    )

    period_start = models.DateField(
        null=True,
        blank=True,
    )

    period_end = models.DateField(
        null=True,
        blank=True,
    )

    computed_at = models.DateTimeField(
        auto_now_add=True,
    )

    dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional breakdowns (department, payer, etc.).",
    )

    class Meta:
        db_table = "rcm_metrics"

        verbose_name = "RCM Metric"

        verbose_name_plural = "RCM Metrics"

        ordering = (
            "category",
            "name",
            "-computed_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "category",
                    "name",
                ],
                name="metric_org_cat_name_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.name} = {self.value} {self.unit}"


__all__ = [
    "RcmMetric",
]
