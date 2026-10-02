"""Revenue Cycle Eligibility aggregate model."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.eligibility.constants import CoverageStatus, EligibilityStatus


class Eligibility(BaseModel):
    """Store an organization-scoped insurance eligibility verification."""

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="revenue_cycle_eligibility"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="revenue_cycle_eligibility"
    )
    payer_id = models.CharField(max_length=100, db_index=True)
    payer_name = models.CharField(max_length=255, blank=True)
    member_id = models.CharField(max_length=100, db_index=True)
    group_number = models.CharField(max_length=100, blank=True)
    subscriber_name = models.CharField(max_length=255, blank=True)
    subscriber_relationship = models.CharField(max_length=50, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    coverage_start = models.DateField(null=True, blank=True)
    coverage_end = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=30,
        choices=[(x.value, x.value) for x in EligibilityStatus],
        default=EligibilityStatus.PENDING.value,
        db_index=True,
    )
    coverage_status = models.CharField(
        max_length=30,
        choices=[(x.value, x.value) for x in CoverageStatus],
        default=CoverageStatus.UNKNOWN.value,
        db_index=True,
    )
    copay_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    deductible_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    response_code = models.CharField(max_length=100, blank=True)
    response_message = models.TextField(blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    request_reference = models.CharField(max_length=100, db_index=True)
    idempotency_key = models.CharField(max_length=255, db_index=True)
    failure_reason = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_eligibility_verified",
    )

    class Meta:
        """Database metadata for Eligibility."""

        db_table = "revenue_cycle_eligibility"
        ordering = ("-requested_at",)
        indexes = (
            models.Index(
                fields=("organization", "patient", "-requested_at"),
                name="rc_elig_patient_req_idx",
            ),
            models.Index(
                fields=("organization", "status"), name="rc_elig_org_status_idx"
            ),
            models.Index(
                fields=("organization", "payer_id", "member_id"),
                name="rc_elig_org_payer_member_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_elig_org_idempotency_uniq",
            ),
        )

    def __str__(self) -> str:
        """Return a stable representation."""
        return f"{self.payer_id}:{self.member_id}:{self.request_reference}"


__all__ = ("Eligibility",)
