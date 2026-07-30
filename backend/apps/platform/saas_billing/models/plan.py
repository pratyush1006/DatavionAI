"""
SaaS subscription plan model.

Defines DatavionOS pricing tiers,
healthcare segments, feature entitlements,
usage limits and subscription capabilities.

Supports:

- Hospitals
- Clinics
- Pharmacies
- Medical Stores
- Laboratories
- Imaging Centers
- Dental Clinics
- Physiotherapy Centers
- Healthcare Enterprises
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.plan import (
    PlanManager,
)


class Plan(BaseModel):
    """
    DatavionOS SaaS subscription plan.

    Examples:

    - Starter Clinic
    - Pharmacy Pro
    - Hospital Enterprise
    - Healthcare Network
    """

    objects = PlanManager()

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class BillingCycle(models.TextChoices):
        MONTHLY = (
            "monthly",
            _("Monthly"),
        )

        YEARLY = (
            "yearly",
            _("Yearly"),
        )

    class Currency(models.TextChoices):
        USD = (
            "USD",
            _("US Dollar"),
        )

        INR = (
            "INR",
            _("Indian Rupee"),
        )

        EUR = (
            "EUR",
            _("Euro"),
        )

        GBP = (
            "GBP",
            _("British Pound"),
        )

    class PlanType(models.TextChoices):
        STARTER = (
            "STARTER",
            _("Starter"),
        )

        PROFESSIONAL = (
            "PROFESSIONAL",
            _("Professional"),
        )

        BUSINESS = (
            "BUSINESS",
            _("Business"),
        )

        ENTERPRISE = (
            "ENTERPRISE",
            _("Enterprise"),
        )

        CUSTOM = (
            "CUSTOM",
            _("Custom Enterprise"),
        )

    class HealthcareSegment(models.TextChoices):
        HOSPITAL = (
            "HOSPITAL",
            _("Hospital"),
        )

        CLINIC = (
            "CLINIC",
            _("Clinic"),
        )

        PHARMACY = (
            "PHARMACY",
            _("Pharmacy / Medical Store"),
        )

        LABORATORY = (
            "LABORATORY",
            _("Diagnostic Laboratory"),
        )

        IMAGING = (
            "IMAGING",
            _("Imaging Center"),
        )

        DENTAL = (
            "DENTAL",
            _("Dental Clinic"),
        )

        PHYSIOTHERAPY = (
            "PHYSIOTHERAPY",
            _("Physiotherapy Center"),
        )

        NURSING_HOME = (
            "NURSING_HOME",
            _("Nursing Home"),
        )

        ENTERPRISE = (
            "ENTERPRISE",
            _("Healthcare Enterprise"),
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    name = models.CharField(
        max_length=150,
    )

    code = models.SlugField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    plan_type = models.CharField(
        max_length=30,
        choices=PlanType.choices,
        default=PlanType.STARTER,
        db_index=True,
    )

    healthcare_segment = models.CharField(
        max_length=50,
        choices=HealthcareSegment.choices,
        default=HealthcareSegment.CLINIC,
        db_index=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    # ------------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------------

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    setup_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.INR,
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
    )

    trial_days = models.PositiveIntegerField(
        default=14,
    )

    annual_discount_percentage = models.PositiveIntegerField(
        default=0,
    )

    # ------------------------------------------------------------------
    # Organization Limits
    # ------------------------------------------------------------------

    max_users = models.PositiveIntegerField(
        default=5,
    )

    max_branches = models.PositiveIntegerField(
        default=1,
    )

    max_doctors = models.PositiveIntegerField(
        default=5,
    )

    # ------------------------------------------------------------------
    # Healthcare Limits
    # ------------------------------------------------------------------

    max_patients = models.PositiveBigIntegerField(
        default=1000,
    )

    max_lab_orders = models.PositiveIntegerField(
        default=1000,
    )

    max_imaging_orders = models.PositiveIntegerField(
        default=1000,
    )

    # ------------------------------------------------------------------
    # Pharmacy Limits
    # ------------------------------------------------------------------

    max_pharmacy_products = models.PositiveIntegerField(
        default=1000,
    )

    max_inventory_transactions = models.PositiveIntegerField(
        default=10000,
    )

    # ------------------------------------------------------------------
    # Platform Limits
    # ------------------------------------------------------------------

    max_storage_gb = models.PositiveIntegerField(
        default=5,
    )

    max_api_requests = models.PositiveBigIntegerField(
        default=10000,
    )

    # ------------------------------------------------------------------
    # AI Limits
    # ------------------------------------------------------------------

    max_ai_requests = models.PositiveBigIntegerField(
        default=1000,
    )

    max_ai_tokens = models.PositiveBigIntegerField(
        default=100000,
    )

    # ------------------------------------------------------------------
    # Entitlements
    # ------------------------------------------------------------------

    features = models.JSONField(
        default=dict,
        blank=True,
    )

    modules = models.JSONField(
        default=dict,
        blank=True,
    )

    limits = models.JSONField(
        default=dict,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_default = models.BooleanField(
        default=False,
        help_text=_(
            "Default plan assigned during signup.",
        ),
    )

    is_custom = models.BooleanField(
        default=False,
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        db_table = "saas_billing_plans"

        verbose_name = _(
            "SaaS Billing Plan",
        )

        verbose_name_plural = _(
            "SaaS Billing Plans",
        )

        ordering = (
            "display_order",
            "price",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "code",
                ],
            ),
            models.Index(
                fields=[
                    "plan_type",
                ],
            ),
            models.Index(
                fields=[
                    "healthcare_segment",
                ],
            ),
            models.Index(
                fields=[
                    "is_active",
                    "is_public",
                ],
            ),
        ]

    # ------------------------------------------------------------------
    # Entitlement Helpers
    # ------------------------------------------------------------------

    def has_feature(
        self,
        feature: str,
    ) -> bool:
        """
        Check feature entitlement.
        """

        return bool(
            self.features.get(
                feature,
                False,
            )
        )

    def has_module(
        self,
        module: str,
    ) -> bool:
        """
        Check module entitlement.
        """

        return bool(
            self.modules.get(
                module,
                False,
            )
        )

    def get_usage_limit(
        self,
        metric_type: str,
    ) -> dict:
        """
        Return usage entitlement configuration.

        Example:

        {
            "included": 1000,
            "overage_rate": "0.02",
            "unit": "request"
        }

        Used by:

        - EvaluateUsageWorkflow
        - ChargeUsageWorkflow
        - Usage billing engine
        """

        return self.limits.get(
            metric_type,
            {},
        )

    def __str__(
        self,
    ) -> str:

        return self.name


__all__ = [
    "Plan",
]
