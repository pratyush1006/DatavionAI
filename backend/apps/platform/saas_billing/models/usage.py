"""
SaaS usage tracking model.

Tracks DatavionOS resource consumption
for subscription limits, analytics and
usage based billing.

Supports:

- Hospitals
- Clinics
- Pharmacies
- Medical Stores
- Laboratories
- Healthcare Networks
- AI workloads
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.usage import (
    UsageManager,
)


class Usage(BaseModel):
    """
    Organization resource consumption.

    Used for:

    - quota enforcement
    - subscription limits
    - usage billing
    - analytics
    - AI metering
    """

    objects = UsageManager()

    class MetricType(models.TextChoices):
        # --------------------------------------------------------------
        # Organization
        # --------------------------------------------------------------

        USERS = (
            "USERS",
            _("Users"),
        )

        STORAGE_GB = (
            "STORAGE_GB",
            _("Storage GB"),
        )

        API_CALLS = (
            "API_CALLS",
            _("API Calls"),
        )

        # --------------------------------------------------------------
        # Healthcare
        # --------------------------------------------------------------

        PATIENTS = (
            "PATIENTS",
            _("Patients"),
        )

        APPOINTMENTS = (
            "APPOINTMENTS",
            _("Appointments"),
        )

        ENCOUNTERS = (
            "ENCOUNTERS",
            _("Clinical Encounters"),
        )

        PRESCRIPTIONS = (
            "PRESCRIPTIONS",
            _("Prescriptions"),
        )

        LAB_ORDERS = (
            "LAB_ORDERS",
            _("Laboratory Orders"),
        )

        IMAGING_STUDIES = (
            "IMAGING_STUDIES",
            _("Imaging Studies"),
        )

        TELEMEDICINE_MINUTES = (
            "TELEMEDICINE_MINUTES",
            _("Telemedicine Minutes"),
        )

        # --------------------------------------------------------------
        # Pharmacy / Medical Store
        # --------------------------------------------------------------

        PHARMACY_ORDERS = (
            "PHARMACY_ORDERS",
            _("Pharmacy Orders"),
        )

        INVENTORY_TRANSACTIONS = (
            "INVENTORY_TRANSACTIONS",
            _("Inventory Transactions"),
        )

        BILLING_TRANSACTIONS = (
            "BILLING_TRANSACTIONS",
            _("Billing Transactions"),
        )

        # --------------------------------------------------------------
        # AI Platform
        # --------------------------------------------------------------

        AI_REQUESTS = (
            "AI_REQUESTS",
            _("AI Requests"),
        )

        AI_TOKENS = (
            "AI_TOKENS",
            _("AI Tokens"),
        )

        AI_DOCUMENTS = (
            "AI_DOCUMENTS",
            _("AI Documents Processed"),
        )

        WORKFLOW_EXECUTIONS = (
            "WORKFLOW_EXECUTIONS",
            _("Workflow Executions"),
        )

        AUTOMATIONS = (
            "AUTOMATIONS",
            _("Automation Executions"),
        )

    # ==============================================================
    # Ownership
    # ==============================================================

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="usage_records",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_usage",
    )

    # ==============================================================
    # Metric
    # ==============================================================

    metric_type = models.CharField(
        max_length=50,
        choices=MetricType.choices,
        db_index=True,
    )

    value = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        default=0,
        help_text=_(
            "Measured usage value.",
        ),
    )

    unit = models.CharField(
        max_length=50,
        default="count",
    )

    # ==============================================================
    # Billing Metering
    # ==============================================================

    is_billable = models.BooleanField(
        default=False,
        db_index=True,
    )

    billing_rate = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=0,
        help_text=_(
            "Cost per usage unit.",
        ),
    )

    calculated_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        help_text=_(
            "Calculated billing amount.",
        ),
    )

    # ==============================================================
    # Subscription Period
    # ==============================================================

    period_start = models.DateTimeField(
        db_index=True,
    )

    period_end = models.DateTimeField(
        db_index=True,
    )

    # ==============================================================
    # Source Tracking
    # ==============================================================

    source = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "DatavionOS module generating usage.",
        ),
    )

    reference_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "Related business object identifier.",
        ),
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ==============================================================
    # Meta
    # ==============================================================

    class Meta:
        db_table = "saas_usage"

        verbose_name = _(
            "SaaS Usage",
        )

        verbose_name_plural = _(
            "SaaS Usage Records",
        )

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "metric_type",
                ],
            ),
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
            models.Index(
                fields=[
                    "is_billable",
                ],
            ),
            models.Index(
                fields=[
                    "reference_id",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "metric_type",
                    "period_start",
                    "period_end",
                ],
                name=("unique_usage_period_metric"),
            ),
        ]

    def calculate_cost(
        self,
    ):
        """
        Calculate billable usage cost.
        """

        self.calculated_cost = self.value * self.billing_rate

        return self.calculated_cost

    def __str__(
        self,
    ) -> str:

        return f"{self.organization} - {self.metric_type}"


__all__ = [
    "Usage",
]
