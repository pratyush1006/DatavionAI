"""Domain services for Revenue Cycle Eligibility."""

from __future__ import annotations

from datetime import date
from typing import Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from apps.revenue_cycle.eligibility.constants import CoverageStatus, EligibilityStatus
from apps.revenue_cycle.eligibility.exceptions import (
    EligibilityInvariantError,
    EligibilityTransitionError,
)
from apps.revenue_cycle.eligibility.models import Eligibility

_ALLOWED_TRANSITIONS = {
    EligibilityStatus.PENDING.value: {
        EligibilityStatus.IN_PROGRESS.value,
        EligibilityStatus.FAILED.value,
    },
    EligibilityStatus.IN_PROGRESS.value: {
        EligibilityStatus.VERIFIED.value,
        EligibilityStatus.FAILED.value,
    },
    EligibilityStatus.VERIFIED.value: {EligibilityStatus.INACTIVE.value},
    EligibilityStatus.FAILED.value: {EligibilityStatus.PENDING.value},
    EligibilityStatus.INACTIVE.value: set(),
}


class EligibilityService:
    """Own Eligibility mutations and invariants."""

    @staticmethod
    def _validate_patient(*, patient, organization) -> None:
        """Ensure canonical Patient belongs to the organization and is active."""
        if patient.organization_id != organization.pk or patient.is_deleted:
            raise EligibilityInvariantError(
                "Patient is not valid for this organization."
            )

    @classmethod
    def create(cls, *, patient, organization, performed_by, **data: Any) -> Eligibility:
        """Create one idempotent Eligibility request."""
        cls._validate_patient(patient=patient, organization=organization)
        for field in ("payer_id", "member_id", "request_reference", "idempotency_key"):
            if not str(data.get(field, "")).strip():
                raise ValidationError({field: "This field is required."})
        obj = Eligibility(
            patient=patient,
            organization=organization,
            payer_id=str(data["payer_id"]).strip(),
            payer_name=str(data.get("payer_name", "")).strip(),
            member_id=str(data["member_id"]).strip(),
            group_number=str(data.get("group_number", "")).strip(),
            subscriber_name=str(data.get("subscriber_name", "")).strip(),
            subscriber_relationship=str(
                data.get("subscriber_relationship", "")
            ).strip(),
            request_reference=str(data["request_reference"]).strip(),
            idempotency_key=str(data["idempotency_key"]).strip(),
            response_payload=dict(data.get("response_payload") or {}),
        )
        try:
            obj.full_clean()
            obj.save()
        except IntegrityError as exc:
            raise EligibilityInvariantError(
                "An eligibility request with this idempotency key already exists."
            ) from exc
        return obj

    @staticmethod
    def update(*, eligibility, performed_by, **data: Any) -> Eligibility:
        """Update only mutable Eligibility metadata."""
        protected = {
            "organization_id",
            "patient_id",
            "status",
            "coverage_status",
            "requested_at",
            "verified_at",
            "verified_by_id",
            "idempotency_key",
            "request_reference",
        }
        forbidden = protected.intersection(data)
        if forbidden:
            raise ValidationError(
                "Protected Eligibility fields cannot be modified: "
                + ", ".join(sorted(forbidden))
            )
        for field in (
            "payer_id",
            "payer_name",
            "member_id",
            "group_number",
            "subscriber_name",
            "subscriber_relationship",
            "response_code",
            "response_message",
            "failure_reason",
        ):
            if field in data:
                setattr(eligibility, field, str(data[field]).strip())
        if "response_payload" in data:
            eligibility.response_payload = dict(data["response_payload"] or {})
        eligibility.full_clean()
        eligibility.save()
        return eligibility

    @staticmethod
    def transition(*, eligibility, status: str, performed_by) -> Eligibility:
        """Apply a strict lifecycle transition."""
        target = str(status).strip().lower()
        if target not in _ALLOWED_TRANSITIONS.get(eligibility.status, set()):
            raise EligibilityTransitionError(
                f"Cannot transition Eligibility from {eligibility.status!r} to {target!r}."
            )
        eligibility.status = target
        if target == EligibilityStatus.VERIFIED.value:
            eligibility.verified_at = timezone.now()
            eligibility.verified_by = performed_by
        if target == EligibilityStatus.FAILED.value:
            eligibility.verified_at = None
            eligibility.verified_by = None
        eligibility.save()
        return eligibility

    @staticmethod
    def record_response(
        *,
        eligibility,
        performed_by,
        coverage_status: str,
        response_code: str = "",
        response_message: str = "",
        response_payload: dict[str, Any] | None = None,
        coverage_start: date | None = None,
        coverage_end: date | None = None,
        copay_amount=None,
        deductible_amount=None,
    ) -> Eligibility:
        """Persist a normalized payer response."""
        normalized = str(coverage_status).strip().lower()
        if normalized not in {x.value for x in CoverageStatus}:
            raise ValidationError({"coverage_status": "Unsupported coverage status."})
        if coverage_start and coverage_end and coverage_end < coverage_start:
            raise ValidationError(
                {"coverage_end": "Coverage end cannot precede coverage start."}
            )
        eligibility.coverage_status = normalized
        eligibility.response_code = str(response_code).strip()
        eligibility.response_message = str(response_message).strip()
        eligibility.response_payload = dict(response_payload or {})
        eligibility.coverage_start = coverage_start
        eligibility.coverage_end = coverage_end
        eligibility.copay_amount = copay_amount
        eligibility.deductible_amount = deductible_amount
        if normalized != CoverageStatus.UNKNOWN.value:
            eligibility.status = EligibilityStatus.VERIFIED.value
            eligibility.verified_at = timezone.now()
            eligibility.verified_by = performed_by
        eligibility.full_clean()
        eligibility.save()
        return eligibility

    @staticmethod
    def delete(*, eligibility, performed_by) -> Eligibility:
        """Soft-delete an Eligibility record."""
        eligibility.delete(user_id=performed_by.pk)
        return eligibility

    @staticmethod
    def restore(*, eligibility, performed_by) -> Eligibility:
        """Restore a deleted Eligibility record."""
        eligibility.restore()
        eligibility.save()
        return eligibility


__all__ = ("EligibilityService",)
