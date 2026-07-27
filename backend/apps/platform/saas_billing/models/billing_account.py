"""
SaaS billing account model.

Stores billing identity and payment
provider information for DatavionOS
organizations.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class BillingAccount(BaseModel):
    """
    Billing profile for a SaaS organization.

    Used for:

    - subscription billing
    - invoices
    - payment providers
    - tax information
    """

    class Currency(models.TextChoices):
        """
        Supported billing currencies.
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

        GBP = (
            "GBP",
            _("British Pound"),
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
    # Legal Billing Identity
    # ------------------------------------------------------------------

    legal_name = models.CharField(
        max_length=255,
        help_text=_(
            "Legal billing entity name.",
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
        help_text=_(
            "Billing contact phone number.",
        ),
    )

    tax_id = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Tax identification number.",
        ),
    )

    gst_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "GST registration number.",
        ),
    )

    vat_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "VAT registration number.",
        ),
    )

    # ------------------------------------------------------------------
    # Currency
    # ------------------------------------------------------------------

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.USD,
        help_text=_(
            "Billing currency.",
        ),
    )

    billing_address = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Billing address information.",
        ),
    )

    # ------------------------------------------------------------------
    # Payment Provider
    # ------------------------------------------------------------------

    payment_provider = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Payment provider name.",
        ),
    )

    payment_customer_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "External payment customer ID.",
        ),
    )

    default_payment_method_id = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            "Default payment method reference.",
        ),
    )

    auto_charge_enabled = models.BooleanField(
        default=False,
        help_text=_(
            "Enable automatic payment collection.",
        ),
    )

    configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Additional billing configuration.",
        ),
    )

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
                    "payment_customer_id",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"Billing Account - {self.organization}"


__all__ = [
    "BillingAccount",
]
