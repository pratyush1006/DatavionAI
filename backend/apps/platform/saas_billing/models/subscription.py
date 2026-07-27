"""
SaaS subscription model.

Manages organization subscriptions
against DatavionOS plans.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Subscription(BaseModel):
    """
    Represents an organization's SaaS subscription.

    Relationship:

        Organization
              |
              |
        Subscription
              |
              |
             Plan
    """

    class Status(models.TextChoices):
        """
        Subscription lifecycle states.
        """

        TRIAL = (
            "trial",
            _("Trial"),
        )

        ACTIVE = (
            "active",
            _("Active"),
        )

        PAST_DUE = (
            "past_due",
            _("Past Due"),
        )

        SUSPENDED = (
            "suspended",
            _("Suspended"),
        )

        CANCELLED = (
            "cancelled",
            _("Cancelled"),
        )

        EXPIRED = (
            "expired",
            _("Expired"),
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_subscription",
        help_text=_(
            "Organization owning this subscription.",
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
        help_text=_(
            "Current subscription status.",
        ),
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
        help_text=_(
            "Subscription activation date.",
        ),
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Subscription expiry date.",
        ),
    )

    cancelled_at = models.DateTimeField(
        null=True,
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
    # External Billing
    # ------------------------------------------------------------------

    provider = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Payment provider name.",
        ),
    )

    external_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "External payment provider subscription ID.",
        ),
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Additional subscription metadata.",
        ),
    )

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
                    "status",
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
