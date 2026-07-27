"""
SaaS subscription plan model.

Defines DatavionOS pricing tiers and feature limits.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Plan(BaseModel):
    """
    Represents a SaaS subscription plan.

    Example:

    Starter
    Professional
    Enterprise
    """

    class BillingCycle(models.TextChoices):
        """
        Supported billing cycles.
        """

        MONTHLY = (
            "monthly",
            _("Monthly"),
        )

        YEARLY = (
            "yearly",
            _("Yearly"),
        )

    class Currency(models.TextChoices):
        """
        Supported currencies.
        """

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

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    name = models.CharField(
        max_length=150,
        help_text=_(
            "Human readable plan name.",
        ),
    )

    code = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_(
            "Unique plan identifier.",
        ),
    )

    description = models.TextField(
        blank=True,
        help_text=_(
            "Plan description.",
        ),
    )

    # ------------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------------

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text=_(
            "Plan price.",
        ),
    )

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.USD,
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
    )

    # ------------------------------------------------------------------
    # SaaS Limits
    # ------------------------------------------------------------------

    max_users = models.PositiveIntegerField(
        default=5,
        help_text=_(
            "Maximum organization users.",
        ),
    )

    max_storage_gb = models.PositiveIntegerField(
        default=5,
        help_text=_(
            "Storage quota in GB.",
        ),
    )

    max_patients = models.PositiveBigIntegerField(
        default=1000,
        help_text=_(
            "Maximum patient records.",
        ),
    )

    # ------------------------------------------------------------------
    # Feature Control
    # ------------------------------------------------------------------

    features = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Enabled platform features.",
        ),
    )

    modules = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Enabled DatavionOS modules.",
        ),
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_(
            "Whether this plan is available.",
        ),
    )

    is_public = models.BooleanField(
        default=True,
        help_text=_(
            "Whether customers can select this plan.",
        ),
    )

    class Meta:
        db_table = "saas_billing_plans"

        verbose_name = _(
            "SaaS Billing Plan",
        )

        verbose_name_plural = _(
            "SaaS Billing Plans",
        )

        ordering = (
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
                    "is_active",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return self.name


__all__ = [
    "Plan",
]
