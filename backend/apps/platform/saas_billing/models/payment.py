"""
SaaS payment model.

Tracks payments, refunds,
gateway transactions and reconciliation
for DatavionOS subscriptions.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.payment import (
    PaymentManager,
)


class Payment(BaseModel):
    """
    Enterprise SaaS payment transaction.

    Supports:

    - Stripe
    - Razorpay
    - PayPal
    - Bank transfer
    - Enterprise invoices
    - Refund workflows
    """

    objects = PaymentManager()

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class Status(models.TextChoices):
        PENDING = (
            "PENDING",
            _("Pending"),
        )

        PROCESSING = (
            "PROCESSING",
            _("Processing"),
        )

        SUCCESS = (
            "SUCCESS",
            _("Success"),
        )

        FAILED = (
            "FAILED",
            _("Failed"),
        )

        CANCELLED = (
            "CANCELLED",
            _("Cancelled"),
        )

        REFUNDED = (
            "REFUNDED",
            _("Refunded"),
        )

        PARTIALLY_REFUNDED = (
            "PARTIALLY_REFUNDED",
            _("Partially Refunded"),
        )

    class Provider(models.TextChoices):
        STRIPE = (
            "STRIPE",
            _("Stripe"),
        )

        RAZORPAY = (
            "RAZORPAY",
            _("Razorpay"),
        )

        PAYPAL = (
            "PAYPAL",
            _("PayPal"),
        )

        BANK = (
            "BANK",
            _("Bank Transfer"),
        )

        MANUAL = (
            "MANUAL",
            _("Manual"),
        )

    class PaymentMethod(models.TextChoices):
        CARD = (
            "CARD",
            _("Card"),
        )

        UPI = (
            "UPI",
            _("UPI"),
        )

        NET_BANKING = (
            "NET_BANKING",
            _("Net Banking"),
        )

        BANK_TRANSFER = (
            "BANK_TRANSFER",
            _("Bank Transfer"),
        )

        WALLET = (
            "WALLET",
            _("Wallet"),
        )

        OTHER = (
            "OTHER",
            _("Other"),
        )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="payments",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_payments",
    )

    invoice = models.ForeignKey(
        "saas_billing.Invoice",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    # ------------------------------------------------------------------
    # Payment Details
    # ------------------------------------------------------------------

    provider = models.CharField(
        max_length=50,
        choices=Provider.choices,
        blank=True,
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        blank=True,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    gateway_payment_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "Payment gateway payment identifier.",
        ),
    )

    gateway_order_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Amount
    # ------------------------------------------------------------------

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    refunded_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="INR",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    refunded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------------------
    # Gateway / Accounting
    # ------------------------------------------------------------------

    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Raw payment gateway response.",
        ),
    )

    reconciliation_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Accounting reconciliation information.",
        ),
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

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
                    "tenant",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "invoice",
                ],
            ),
            models.Index(
                fields=[
                    "transaction_id",
                ],
            ),
            models.Index(
                fields=[
                    "gateway_payment_id",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:

        return f"{self.organization} - {self.amount} {self.currency}"


__all__ = [
    "Payment",
]
