"""
SaaS usage tracking model.

Tracks organization resource consumption
for subscription limits and billing.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Usage(BaseModel):
    """
    Tracks SaaS resource usage for an organization.

    Used for:

    - quota enforcement
    - billing calculations
    - analytics
    - plan limits
    """

    class MetricType(models.TextChoices):
        """
        Supported usage metrics.
        """

        USERS = (
            "users",
            _("Users"),
        )

        STORAGE = (
            "storage",
            _("Storage"),
        )

        PATIENTS = (
            "patients",
            _("Patients"),
        )

        DOCUMENTS = (
            "documents",
            _("Documents"),
        )

        AI_REQUESTS = (
            "ai_requests",
            _("AI Requests"),
        )

        AI_TOKENS = (
            "ai_tokens",
            _("AI Tokens"),
        )

        API_CALLS = (
            "api_calls",
            _("API Calls"),
        )

        WORKFLOW_EXECUTIONS = (
            "workflow_executions",
            _("Workflow Executions"),
        )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_usage",
        help_text=_(
            "Organization using the resource.",
        ),
    )

    metric_type = models.CharField(
        max_length=50,
        choices=MetricType.choices,
        db_index=True,
        help_text=_(
            "Usage metric type.",
        ),
    )

    value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        help_text=_(
            "Current usage value.",
        ),
    )

    unit = models.CharField(
        max_length=50,
        default="count",
        help_text=_(
            "Measurement unit.",
        ),
    )

    period_start = models.DateTimeField(
        help_text=_(
            "Usage period start.",
        ),
    )

    period_end = models.DateTimeField(
        help_text=_(
            "Usage period end.",
        ),
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Additional usage metadata.",
        ),
    )

    class Meta:
        db_table = "saas_usage"

        verbose_name = _(
            "SaaS Usage",
        )

        verbose_name_plural = _(
            "SaaS Usage Records",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "metric_type",
                ],
            ),
            models.Index(
                fields=[
                    "period_start",
                    "period_end",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.organization} - {self.metric_type}"


__all__ = [
    "Usage",
]
