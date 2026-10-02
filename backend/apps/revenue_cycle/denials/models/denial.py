"""Denial aggregate model."""

from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.denials.constants import DenialPriority, DenialStatus


class Denial(BaseModel):
    """Represent a payer denial requiring revenue-cycle resolution."""

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="revenue_cycle_denials"
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_denials",
    )
    claim_submission_id = models.UUIDField(null=True, blank=True, db_index=True)
    external_claim_id = models.CharField(max_length=100, blank=True)
    payer_name = models.CharField(max_length=255)
    denial_code = models.CharField(max_length=50, db_index=True)
    denial_reason = models.TextField()
    amount = models.DecimalField(
        max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    status = models.CharField(
        max_length=30,
        choices=DenialStatus.choices,
        default=DenialStatus.OPEN,
        db_index=True,
    )
    priority = models.CharField(
        max_length=20,
        choices=DenialPriority.choices,
        default=DenialPriority.NORMAL,
        db_index=True,
    )
    received_at = models.DateTimeField()
    due_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(blank=True)
    external_reference = models.CharField(max_length=100, blank=True)
    idempotency_key = models.CharField(max_length=128)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_revenue_cycle_denials",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Denial database metadata."""

        db_table = "revenue_cycle_denials"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_denial_org_idempotency_uniq",
            ),
        )
        indexes = (
            models.Index(fields=("organization", "status")),
            models.Index(fields=("organization", "patient", "received_at")),
            models.Index(fields=("organization", "denial_code")),
        )


__all__ = ("Denial",)
