"""
SaaS payment model.

Tracks payments received for
DatavionOS subscriptions.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Payment(BaseModel):
    """
    Payment record for SaaS invoices.

    Represents payment made by an organization
    towards DatavionOS subscription invoices.
    """

    class Status(models.TextChoices):
        """
        Payment lifecycle states.
        """

        PENDING = (
            "pending",
            _("Pending"),
        )

        SUCCESS = (
            "success",
            _("Success"),
        )

        FAILED = (
            "failed",
            _("Failed"),
        )

        REFUNDED = (
            "refunded",
            _("Refunded"),
        )

    class Provider(models.TextChoices):
        """
        Supported payment providers.
        """

        STRIPE = (
            "stripe",
            _("Stripe"),
        )

        RAZORPAY = (
            "razorpay",
            _("Razorpay"),
        )

        PAYPAL = (
            "paypal",
            _("PayPal"),
        )

        BANK = (
            "bank",
            _("Bank Transfer"),
        )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_payments",
        help_text=_(
            "Organization making payment.",
        ),
    )

    invoice = models.ForeignKey(
        "saas_billing.Invoice",
        on_delete=models.PROTECT,
        related_name="payments",
        help_text=_(
            "Invoice being paid.",
        ),
    )

    # ------------------------------------------------------------------
    # Payment Information
    # ------------------------------------------------------------------

    provider = models.CharField(
        max_length=50,
        choices=Provider.choices,
        blank=True,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "External transaction identifier.",
        ),
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text=_(
            "Payment amount.",
        ),
    )

    currency = models.CharField(
        max_length=10,
        default="USD",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Additional payment metadata.",
        ),
    )

    class Meta:
        db_table = "saas_payments"

        verbose_name = _(
            "SaaS Payment",
        )

        verbose_name_plural = _(
            "SaaS Payments",
        )

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "transaction_id",
                ],
            ),
            models.Index(
                fields=[
                    "invoice",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.organization} - {self.amount}"


__all__ = [
    "Payment",
]
