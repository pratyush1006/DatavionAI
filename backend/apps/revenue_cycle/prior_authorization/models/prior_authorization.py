"""Revenue Cycle Prior Authorization aggregate model."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationMethod,
    AuthorizationOutcome,
    AuthorizationStatus,
)


class PriorAuthorization(BaseModel):
    """Store an organization-scoped prior authorization request and decision."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_prior_authorizations",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="revenue_cycle_prior_authorizations",
    )
    eligibility_reference = models.UUIDField(null=True, blank=True, db_index=True)
    payer_id = models.CharField(max_length=100, db_index=True)
    payer_name = models.CharField(max_length=255, blank=True)
    member_id = models.CharField(max_length=100, db_index=True)
    policy_number = models.CharField(max_length=100, blank=True)
    group_number = models.CharField(max_length=100, blank=True)
    procedure_code = models.CharField(max_length=50, db_index=True)
    service_description = models.CharField(max_length=500, blank=True)
    place_of_service = models.CharField(max_length=20, blank=True)
    rendering_provider_npi = models.CharField(max_length=20, blank=True)
    clinical_indication = models.TextField(blank=True)
    authorization_method = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationMethod),
        default=AuthorizationMethod.MANUAL.value,
    )
    status = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationStatus),
        default=AuthorizationStatus.PENDING.value,
        db_index=True,
    )
    outcome = models.CharField(
        max_length=30,
        choices=tuple((item.value, item.value) for item in AuthorizationOutcome),
        default=AuthorizationOutcome.UNKNOWN.value,
        db_index=True,
    )
    requested_service_date = models.DateField(null=True, blank=True)
    requested_units = models.PositiveIntegerField(null=True, blank=True)
    approved_units = models.PositiveIntegerField(null=True, blank=True)
    requested_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    authorization_number = models.CharField(max_length=100, blank=True, db_index=True)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    decision_reason = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    response_code = models.CharField(max_length=100, blank=True)
    response_message = models.TextField(blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    request_reference = models.CharField(max_length=100, db_index=True)
    idempotency_key = models.CharField(max_length=255, db_index=True)
    failure_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_prior_authorizations_approved",
    )

    class Meta:
        """Database metadata for Prior Authorization."""

        db_table = "revenue_cycle_prior_authorization"
        ordering = ("-requested_at",)
        indexes = (
            models.Index(
                fields=("organization", "patient", "-requested_at"),
                name="rc_pa_org_patient_req_idx",
            ),
            models.Index(
                fields=("organization", "status"),
                name="rc_pa_org_status_idx",
            ),
            models.Index(
                fields=("organization", "payer_id", "member_id"),
                name="rc_pa_org_payer_member_idx",
            ),
            models.Index(
                fields=("organization", "procedure_code", "requested_service_date"),
                name="rc_pa_org_proc_date_idx",
            ),
            models.Index(
                fields=("organization", "outcome"),
                name="rc_pa_org_outcome_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="rc_pa_org_idempotency_uniq",
            ),
        )

    def __str__(self) -> str:
        """Return a stable authorization representation."""

        return f"{self.payer_id}:{self.member_id}:{self.request_reference}"


__all__ = ("PriorAuthorization",)
