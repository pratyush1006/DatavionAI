from __future__ import annotations

"""Coding aggregate persistence model."""

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

from ..constants import DEFAULT_STATUS, CodingStatus, CodingType


class CodingRecord(BaseModel):
    """Represent a coding work item for a canonical patient encounter."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_records",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_records",
    )
    coding_type = models.CharField(
        max_length=32,
        choices=CodingType.choices,
        default=CodingType.PROFESSIONAL,
    )
    status = models.CharField(
        max_length=32,
        choices=CodingStatus.choices,
        default=DEFAULT_STATUS,
        db_index=True,
    )
    source_reference = models.CharField(
        max_length=128,
        db_index=True,
    )
    service_date = models.DateField(db_index=True)
    encounter_type = models.CharField(
        max_length=64,
        blank=True,
    )
    clinical_summary = models.TextField(blank=True)
    documentation = models.JSONField(
        default=dict,
        blank=True,
    )
    coding_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    idempotency_key = models.CharField(max_length=128)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_revenue_cycle_records",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_revenue_cycle_records",
    )
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_revenue_cycle_records",
    )
    released_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="released_revenue_cycle_records",
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "revenue_cycle"
        """Define CodingRecord database metadata."""

        db_table = "revenue_cycle_records"
        ordering = ("-service_date", "-created_at")
        indexes = (
            models.Index(
                fields=("organization", "patient", "service_date"),
                name="rc_coding_org_patient_date_idx",
            ),
            models.Index(
                fields=("organization", "status", "service_date"),
                name="rc_coding_org_status_date_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_coding_org_idempotency_uniq",
            ),
            models.UniqueConstraint(
                fields=("organization", "source_reference"),
                condition=models.Q(is_deleted=False),
                name="rc_coding_org_source_active_uniq",
            ),
        )


__all__ = ("CodingRecord",)
