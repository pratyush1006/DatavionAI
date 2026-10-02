"""Electronic Remittance Advice aggregate."""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models.base import BaseModel
from apps.platform.organizations.models import Organization

from ..constants import ERASource, ERAStatus


class ERA(BaseModel):
    """Represent a tenant-scoped electronic remittance advice envelope."""

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="revenue_cycle_eras"
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_eras",
        null=True,
        blank=True,
    )
    payer_name = models.CharField(max_length=200)
    payer_identifier = models.CharField(max_length=100, blank=True)
    trace_number = models.CharField(max_length=100)
    check_or_eft_number = models.CharField(max_length=100, blank=True)
    source = models.CharField(
        max_length=20, choices=ERASource.choices, default=ERASource.EDI_835
    )
    status = models.CharField(
        max_length=20,
        choices=ERAStatus.choices,
        default=ERAStatus.RECEIVED,
        db_index=True,
    )
    payment_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    adjustment_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    received_at = models.DateTimeField()
    validated_at = models.DateTimeField(null=True, blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    reversed_at = models.DateTimeField(null=True, blank=True)
    external_reference = models.CharField(max_length=150, blank=True)
    idempotency_key = models.CharField(max_length=150)
    raw_payload = models.JSONField(default=dict, blank=True)
    validation_errors = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_eras",
    )

    class Meta:
        """Configure ERA constraints and indexes."""

        db_table = "revenue_cycle_eras"
        ordering = ("-received_at", "-created_at")
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_era_org_idempotency_uniq",
            ),
            models.UniqueConstraint(
                fields=("organization", "trace_number"), name="rc_era_org_trace_uniq"
            ),
            models.CheckConstraint(
                condition=Q(payment_amount__gte=0), name="rc_era_payment_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(adjustment_amount__gte=0),
                name="rc_era_adjustment_nonnegative",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "status"), name="rc_era_org_status_idx"
            ),
            models.Index(
                fields=("organization", "patient"), name="rc_era_org_patient_idx"
            ),
            models.Index(
                fields=("organization", "received_at"), name="rc_era_org_received_idx"
            ),
        )


__all__ = ("ERA",)
