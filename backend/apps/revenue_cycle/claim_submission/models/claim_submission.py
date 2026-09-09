"""Persistent claim submission aggregate."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models.base import BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_submission.constants import (
    SubmissionMethod,
    SubmissionStatus,
)


class ClaimSubmission(BaseModel):
    """Represent an auditable outbound claim submission."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="revenue_cycle_claim_submissions",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_claim_submissions",
    )
    claim_reference = models.CharField(max_length=100)
    payer_id = models.CharField(max_length=100)
    payer_name = models.CharField(max_length=200, blank=True)
    submission_method = models.CharField(
        max_length=20,
        choices=SubmissionMethod.choices,
        default=SubmissionMethod.EDI,
    )
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
        db_index=True,
    )
    payload = models.JSONField(default=dict, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    external_submission_id = models.CharField(max_length=150, blank=True)
    rejection_code = models.CharField(max_length=100, blank=True)
    rejection_reason = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    idempotency_key = models.CharField(max_length=150)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_revenue_cycle_claim_submissions",
    )

    class Meta:
        """Define database constraints for claim submissions."""

        db_table = "revenue_cycle_claim_submissions"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_claim_submission_org_idempotency_uniq",
            ),
            models.UniqueConstraint(
                fields=("organization", "claim_reference"),
                name="rc_claim_submission_org_reference_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"), name="rc_claim_sub_org_status_idx"
            ),
            models.Index(
                fields=("organization", "patient"), name="rc_claim_sub_org_patient_idx"
            ),
            models.Index(
                fields=("organization", "payer_id"), name="rc_claim_sub_org_payer_idx"
            ),
        ]


__all__ = ("ClaimSubmission",)
