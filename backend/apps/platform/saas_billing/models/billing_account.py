"""
SaaS billing account model.

Stores billing identity, payment provider
configuration and enterprise billing lifecycle.

Architecture:

Tenant
    |
Organization
    |
BillingAccount
    |
Subscription
    |
Invoice
    |
Payment
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.billing import (
    BillingAccountManager,
)


class BillingAccount(BaseModel):
    """
    Enterprise SaaS billing profile.

    Supports:

    - Hospitals
    - Clinics
    - Pharmacies
    - Medical stores
    - Laboratories
    - Diagnostic centers
    - Healthcare networks
    - Enterprise healthcare groups
    """

    objects = BillingAccountManager()

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

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

    class BillingStatus(models.TextChoices):
        ACTIVE = (
            "ACTIVE",
            _("Active"),
        )

        SUSPENDED = (
            "SUSPENDED",
            _("Suspended"),
        )

        CLOSED = (
            "CLOSED",
            _("Closed"),
        )

    class PaymentTerms(models.TextChoices):
        IMMEDIATE = (
            "IMMEDIATE",
            _("Immediate Payment"),
        )

        NET_15 = (
            "NET_15",
            _("Net 15 Days"),
        )

        NET_30 = (
            "NET_30",
            _("Net 30 Days"),
        )

        NET_60 = (
            "NET_60",
            _("Net 60 Days"),
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="billing_accounts",
        help_text=_(
            "Tenant owning billing account.",
        ),
    )

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="billing_account",
        help_text=_(
            "Organization billing account.",
        ),
    )

    # ------------------------------------------------------------------
    # Legal Identity
    # ------------------------------------------------------------------

    legal_name = models.CharField(
        max_length=255,
        help_text=_(
            "Registered legal billing entity name.",
        ),
    )

    billing_email = models.EmailField(
        help_text=_(
            "Primary billing email.",
        ),
    )

    billing_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    billing_contact_name = models.CharField(
        max_length=255,
        blank=True,
    )

    tax_id = models.CharField(
        max_length=100,
        blank=True,
    )

    gst_number = models.CharField(
        max_length=100,
        blank=True,
    )

    vat_number = models.CharField(
        max_length=100,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Billing Configuration
    # ------------------------------------------------------------------

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.INR,
    )

    status = models.CharField(
        max_length=20,
        choices=BillingStatus.choices,
        default=BillingStatus.ACTIVE,
        db_index=True,
    )

    payment_terms = models.CharField(
        max_length=20,
        choices=PaymentTerms.choices,
        default=PaymentTerms.IMMEDIATE,
    )

    billing_address = models.JSONField(
        default=dict,
        blank=True,
    )

    tax_configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Enterprise Billing
    # ------------------------------------------------------------------

    purchase_order_required = models.BooleanField(
        default=False,
    )

    purchase_order_number = models.CharField(
        max_length=100,
        blank=True,
    )

    credit_limit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    grace_period_days = models.PositiveIntegerField(
        default=7,
    )

    accounting_reference = models.CharField(
        max_length=255,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Payment Provider
    # ------------------------------------------------------------------

    payment_provider = models.CharField(
        max_length=50,
        blank=True,
    )

    payment_customer_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    default_payment_method_id = models.CharField(
        max_length=255,
        blank=True,
    )

    auto_charge_enabled = models.BooleanField(
        default=False,
    )

    # ------------------------------------------------------------------
    # Extension
    # ------------------------------------------------------------------

    configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        db_table = "saas_billing_accounts"

        verbose_name = _(
            "SaaS Billing Account",
        )

        verbose_name_plural = _(
            "SaaS Billing Accounts",
        )

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
                    "payment_customer_id",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.organization} Billing Account"


__all__ = [
    "BillingAccount",
]
