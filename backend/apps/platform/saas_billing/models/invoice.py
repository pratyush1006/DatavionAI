"""
SaaS invoice model.

Enterprise billing document generated
for DatavionOS subscriptions.

Supports:

- Hospitals
- Clinics
- Pharmacies
- Medical stores
- Laboratories
- Healthcare networks
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.saas_billing.managers.invoice import (
    InvoiceManager,
)


class Invoice(BaseModel):
    """
    SaaS billing invoice.

    Represents financial obligation
    from DatavionOS to customer organizations.
    """

    objects = InvoiceManager()

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class Status(models.TextChoices):
        DRAFT = (
            "DRAFT",
            _("Draft"),
        )

        ISSUED = (
            "ISSUED",
            _("Issued"),
        )

        SENT = (
            "SENT",
            _("Sent"),
        )

        PARTIALLY_PAID = (
            "PARTIALLY_PAID",
            _("Partially Paid"),
        )

        PAID = (
            "PAID",
            _("Paid"),
        )

        OVERDUE = (
            "OVERDUE",
            _("Overdue"),
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

    class InvoiceType(models.TextChoices):
        SUBSCRIPTION = (
            "SUBSCRIPTION",
            _("Subscription"),
        )

        USAGE = (
            "USAGE",
            _("Usage Based"),
        )

        ADDON = (
            "ADDON",
            _("Addon"),
        )

        CREDIT_NOTE = (
            "CREDIT_NOTE",
            _("Credit Note"),
        )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="invoices",
        help_text=_(
            "Tenant owning invoice.",
        ),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="saas_invoices",
        help_text=_(
            "Organization billed.",
        ),
    )

    subscription = models.ForeignKey(
        "saas_billing.Subscription",
        on_delete=models.PROTECT,
        related_name="invoices",
        help_text=_(
            "Subscription associated with invoice.",
        ),
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    invoice_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    invoice_type = models.CharField(
        max_length=30,
        choices=InvoiceType.choices,
        default=InvoiceType.SUBSCRIPTION,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Billing Period
    # ------------------------------------------------------------------

    billing_period_start = models.DateTimeField(
        null=True,
        blank=True,
    )

    billing_period_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Amounts
    # ------------------------------------------------------------------

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    tax_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    paid_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="INR",
    )

    # ------------------------------------------------------------------
    # Tax Information
    # ------------------------------------------------------------------

    tax_details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "GST/VAT breakdown.",
        ),
    )

    # ------------------------------------------------------------------
    # Dates
    # ------------------------------------------------------------------

    issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Payment Gateway
    # ------------------------------------------------------------------

    payment_reference = models.CharField(
        max_length=255,
        blank=True,
    )

    payment_provider = models.CharField(
        max_length=50,
        blank=True,
    )

    external_invoice_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Documents
    # ------------------------------------------------------------------

    pdf_file = models.FileField(
        upload_to="billing/invoices/",
        blank=True,
        null=True,
    )

    invoice_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Invoice lines and metadata.",
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
        db_table = "saas_invoices"

        verbose_name = _(
            "SaaS Invoice",
        )

        verbose_name_plural = _(
            "SaaS Invoices",
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
                    "invoice_number",
                ],
            ),
            models.Index(
                fields=[
                    "external_invoice_id",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:

        return f"{self.invoice_number} - {self.organization}"


__all__ = [
    "Invoice",
]
