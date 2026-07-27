"""
SaaS invoice model.

Stores invoices generated for
DatavionOS organization subscriptions.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Invoice(BaseModel):
    """
    SaaS subscription invoice.

    Represents billing from DatavionOS
    to tenant organizations.
    """

    class Status(models.TextChoices):
        """
        Invoice lifecycle states.
        """

        DRAFT = (
            "draft",
            _("Draft"),
        )

        ISSUED = (
            "issued",
            _("Issued"),
        )

        PAID = (
            "paid",
            _("Paid"),
        )

        FAILED = (
            "failed",
            _("Failed"),
        )

        CANCELLED = (
            "cancelled",
            _("Cancelled"),
        )

        REFUNDED = (
            "refunded",
            _("Refunded"),
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
            "Subscription related to invoice.",
        ),
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True,
        help_text=_(
            "Unique invoice number.",
        ),
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Amount
    # ------------------------------------------------------------------

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="USD",
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
    # Payment
    # ------------------------------------------------------------------

    payment_reference = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            "External payment reference.",
        ),
    )

    invoice_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Invoice metadata and line items.",
        ),
    )

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
                    "issued_at",
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
