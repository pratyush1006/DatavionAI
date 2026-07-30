"""
SaaS subscription model.

Manages DatavionOS organization subscriptions,
plan assignment, lifecycle, renewal,
feature entitlements and billing state.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.subscription import (
    SubscriptionManager,
)


class Subscription(BaseModel):
    """
    Organization SaaS subscription.

    Architecture:

        Tenant
          |
     Organization
          |
     BillingAccount
          |
     Subscription
          |
          Plan
          |
     Feature Entitlements
    """

    objects = SubscriptionManager()

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class Status(models.TextChoices):
        """
        Subscription lifecycle.
        """

        TRIAL = (
            "TRIAL",
            _("Trial"),
        )

        ACTIVE = (
            "ACTIVE",
            _("Active"),
        )

        PAST_DUE = (
            "PAST_DUE",
            _("Past Due"),
        )

        SUSPENDED = (
            "SUSPENDED",
            _("Suspended"),
        )

        CANCELLED = (
            "CANCELLED",
            _("Cancelled"),
        )

        EXPIRED = (
            "EXPIRED",
            _("Expired"),
        )

    class CancellationReason(models.TextChoices):
        """
        Subscription cancellation reasons.
        """

        CUSTOMER_REQUEST = (
            "CUSTOMER_REQUEST",
            _("Customer Request"),
        )

        PAYMENT_FAILURE = (
            "PAYMENT_FAILURE",
            _("Payment Failure"),
        )

        PLAN_CHANGE = (
            "PLAN_CHANGE",
            _("Plan Change"),
        )

        OTHER = (
            "OTHER",
            _("Other"),
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text=_(
            "Tenant owning subscription.",
        ),
    )

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_subscription",
        help_text=_(
            "Organization subscription.",
        ),
    )

    plan = models.ForeignKey(
        "saas_billing.Plan",
        on_delete=models.PROTECT,
        related_name="subscriptions",
        help_text=_(
            "Subscribed SaaS plan.",
        ),
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.TRIAL,
        db_index=True,
    )

    trial_start = models.DateTimeField(
        null=True,
        blank=True,
    )

    trial_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_period_start = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_period_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    grace_period_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancellation_reason = models.CharField(
        max_length=50,
        choices=CancellationReason.choices,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Renewal
    # ------------------------------------------------------------------

    auto_renew = models.BooleanField(
        default=True,
        help_text=_(
            "Automatically renew subscription.",
        ),
    )

    # ------------------------------------------------------------------
    # Plan Snapshot
    # ------------------------------------------------------------------

    plan_snapshot = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Frozen plan configuration at purchase time.",
        ),
    )

    feature_snapshot = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Feature entitlement snapshot.",
        ),
    )

    # ------------------------------------------------------------------
    # Usage
    # ------------------------------------------------------------------

    seats_used = models.PositiveIntegerField(
        default=0,
    )

    usage_snapshot = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # External Billing
    # ------------------------------------------------------------------

    provider = models.CharField(
        max_length=50,
        blank=True,
    )

    external_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        db_table = "saas_subscriptions"

        verbose_name = _(
            "SaaS Subscription",
        )

        verbose_name_plural = _(
            "SaaS Subscriptions",
        )

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "current_period_end",
                ],
            ),
            models.Index(
                fields=[
                    "expires_at",
                ],
            ),
            models.Index(
                fields=[
                    "external_subscription_id",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:

        return f"{self.organization} - {self.plan.name}"


__all__ = [
    "Subscription",
]
