"""Charge Capture domain model."""

from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models.base import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

from ..constants import ChargeStatus

__all__ = ("Charge",)


class Charge(BaseModel):
    """Represent a billable clinical or operational charge."""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_charges",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_charges",
    )
    tenant_id = models.UUIDField(db_index=True)
    service_code = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total_amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    status = models.CharField(
        max_length=32,
        choices=[(item.value, item.value) for item in ChargeStatus],
        default=ChargeStatus.DRAFT.value,
        db_index=True,
    )
    idempotency_key = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        db_index=True,
    )
    captured_at = models.DateTimeField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    void_reason = models.CharField(max_length=500, blank=True)

    class Meta:
        """Configure database constraints and indexes."""

        db_table = "revenue_cycle_charge_capture_charges"
        ordering = ("-created_at",)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="rc_cc_charge_quantity_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0),
                name="rc_cc_charge_unit_price_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=0),
                name="rc_cc_charge_total_gte_zero",
            ),
        ]
        indexes = [
            models.Index(
                fields=("tenant_id", "organization", "patient"),
                name="rc_cc_charge_scope_idx",
            ),
            models.Index(
                fields=("tenant_id", "status"),
                name="rc_cc_charge_status_idx",
            ),
        ]

    def __str__(self) -> str:
        """Return a stable human-readable charge identifier."""

        return f"{self.service_code}:{self.pk}"
