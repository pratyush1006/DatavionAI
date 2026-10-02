"""
Revenue Cycle Appeals persistence model.
"""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.appeals.constants import AppealStatus


class Appeal(BaseModel):
    """Represent an auditable payer appeal for a patient and claim."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_appeals",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_appeals",
    )
    claim_reference = models.CharField(max_length=120)
    payer_name = models.CharField(max_length=200)
    appeal_number = models.CharField(max_length=100)
    denial_reference = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=32,
        choices=AppealStatus.choices,
        default=AppealStatus.DRAFT,
        db_index=True,
    )
    priority = models.CharField(
        max_length=16,
        default="normal",
        db_index=True,
    )
    reason = models.TextField()
    clinical_summary = models.TextField(blank=True)
    requested_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    approved_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decision_reason = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_revenue_cycle_appeals",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_revenue_cycle_appeals",
    )
    idempotency_key = models.CharField(max_length=120)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        """Define database metadata and tenant-safe constraints."""

        db_table = "revenue_cycle_appeals"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "appeal_number"),
                name="rc_appeal_org_number_unique",
            ),
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_appeal_org_idempotency_unique",
            ),
            models.CheckConstraint(
                condition=models.Q(requested_amount__gte=0),
                name="rc_appeal_requested_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(approved_amount__gte=0),
                name="rc_appeal_approved_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(approved_amount__lte=models.F("requested_amount")),
                name="rc_appeal_approved_lte_requested",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"),
                name="rc_appeal_org_status_idx",
            ),
            models.Index(
                fields=("organization", "claim_reference"),
                name="rc_appeal_org_claim_idx",
            ),
            models.Index(
                fields=("organization", "patient"),
                name="rc_appeal_org_patient_idx",
            ),
        ]


__all__ = ("Appeal",)
