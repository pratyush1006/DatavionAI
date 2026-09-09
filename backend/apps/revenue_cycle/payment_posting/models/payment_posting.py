"""Payment posting aggregate."""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models.base import BaseModel
from apps.platform.organizations.models import Organization

from ..constants import PaymentPostingSource, PaymentPostingStatus


class PaymentPosting(BaseModel):
    """Represent a tenant-scoped payment posting against a patient account."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_payment_postings",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_payment_postings",
    )
    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_payment_postings",
        null=True,
        blank=True,
    )
    payer_name = models.CharField(max_length=200, blank=True)
    payer_claim_reference = models.CharField(max_length=100, blank=True)
    source = models.CharField(
        max_length=20,
        choices=PaymentPostingSource.choices,
        default=PaymentPostingSource.MANUAL,
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentPostingStatus.choices,
        default=PaymentPostingStatus.PENDING,
        db_index=True,
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    adjustment_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    posted_at = models.DateTimeField(null=True, blank=True)
    reversed_at = models.DateTimeField(null=True, blank=True)
    external_reference = models.CharField(max_length=150, blank=True)
    idempotency_key = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_payment_postings",
    )
    reversal_reason = models.TextField(blank=True)

    class Meta:
        """Configure database constraints and indexes."""

        db_table = "revenue_cycle_payment_postings"
        ordering = ("-created_at",)
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_pp_org_idempotency_uniq",
            ),
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="rc_pp_amount_positive",
            ),
            models.CheckConstraint(
                condition=Q(adjustment_amount__gte=0),
                name="rc_pp_adjustment_nonnegative",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "status"),
                name="rc_pp_org_status_idx",
            ),
            models.Index(
                fields=("organization", "patient"),
                name="rc_pp_org_patient_idx",
            ),
            models.Index(
                fields=("organization", "posted_at"),
                name="rc_pp_org_posted_idx",
            ),
        )


__all__ = ("PaymentPosting",)
