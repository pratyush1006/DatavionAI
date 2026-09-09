"""Transactional Insurance Verification domain services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.insurance_verification.constants import (
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.exceptions import (
    InsuranceVerificationInvariantError,
    InsuranceVerificationTransitionError,
)
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from apps.revenue_cycle.insurance_verification.selectors import (
    get_deleted_verification_for_update,
    get_verification_for_update,
)

_ALLOWED_TRANSITIONS = {
    VerificationStatus.PENDING.value: {
        VerificationStatus.IN_PROGRESS.value,
        VerificationStatus.FAILED.value,
    },
    VerificationStatus.IN_PROGRESS.value: {
        VerificationStatus.VERIFIED.value,
        VerificationStatus.FAILED.value,
    },
    VerificationStatus.VERIFIED.value: {
        VerificationStatus.EXPIRED.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.FAILED.value: {
        VerificationStatus.PENDING.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.EXPIRED.value: {
        VerificationStatus.PENDING.value,
        VerificationStatus.INACTIVE.value,
    },
    VerificationStatus.INACTIVE.value: set(),
}


class InsuranceVerificationService:
    """Provide transactional mutations for Insurance Verification."""

    @staticmethod
    def validate_dates(
        *, coverage_start: date | None, coverage_end: date | None
    ) -> None:
        """Reject an invalid coverage interval."""

        if coverage_start and coverage_end and coverage_end < coverage_start:
            raise InsuranceVerificationInvariantError(
                "coverage_end cannot be earlier than coverage_start."
            )

    @staticmethod
    def validate_amounts(
        *,
        copay_amount: Decimal | None,
        deductible_amount: Decimal | None,
        coinsurance_percent: Decimal | None,
    ) -> None:
        """Reject negative monetary values and invalid coinsurance."""

        if copay_amount is not None and copay_amount < 0:
            raise InsuranceVerificationInvariantError(
                "copay_amount cannot be negative."
            )
        if deductible_amount is not None and deductible_amount < 0:
            raise InsuranceVerificationInvariantError(
                "deductible_amount cannot be negative."
            )
        if coinsurance_percent is not None and not 0 <= coinsurance_percent <= 100:
            raise InsuranceVerificationInvariantError(
                "coinsurance_percent must be between 0 and 100."
            )

    @staticmethod
    def validate_patient(*, organization_id: UUID, patient_id: UUID) -> None:
        """Ensure the patient belongs to the target organization."""

        patient = Patient.objects.filter(
            pk=patient_id,
            organization_id=organization_id,
        ).first()
        if patient is None:
            raise InsuranceVerificationInvariantError(
                "Patient does not belong to the target organization or is unavailable."
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization_id: UUID,
        patient_id: UUID,
        request_reference: str,
        idempotency_key: str,
        payer_id: str,
        member_id: str,
        data: dict[str, Any],
    ) -> InsuranceVerification:
        """Create an Insurance Verification transaction atomically."""

        if not request_reference.strip():
            raise InsuranceVerificationInvariantError("request_reference is required.")
        if not idempotency_key.strip():
            raise InsuranceVerificationInvariantError("idempotency_key is required.")
        if not payer_id.strip() or not member_id.strip():
            raise InsuranceVerificationInvariantError(
                "payer_id and member_id are required."
            )

        cls.validate_patient(
            organization_id=organization_id,
            patient_id=patient_id,
        )
        cls.validate_dates(
            coverage_start=data.get("coverage_start"),
            coverage_end=data.get("coverage_end"),
        )
        cls.validate_amounts(
            copay_amount=data.get("copay_amount"),
            deductible_amount=data.get("deductible_amount"),
            coinsurance_percent=data.get("coinsurance_percent"),
        )

        existing = InsuranceVerification.objects.filter(
            organization_id=organization_id,
            idempotency_key=idempotency_key,
        ).first()
        if existing is not None:
            return existing

        return InsuranceVerification.objects.create(
            organization_id=organization_id,
            patient_id=patient_id,
            payer_id=payer_id.strip(),
            member_id=member_id.strip(),
            request_reference=request_reference.strip(),
            idempotency_key=idempotency_key.strip(),
            **data,
        )

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        data: dict[str, Any],
    ) -> InsuranceVerification:
        """Update mutable verification fields under row lock."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        if verification.status in {
            VerificationStatus.VERIFIED.value,
            VerificationStatus.INACTIVE.value,
        }:
            protected = {
                "payer_id",
                "member_id",
                "request_reference",
                "idempotency_key",
            }
            if protected.intersection(data):
                raise InsuranceVerificationInvariantError(
                    "Identity fields cannot be changed after verification."
                )

        if "coverage_start" in data or "coverage_end" in data:
            cls.validate_dates(
                coverage_start=data.get("coverage_start", verification.coverage_start),
                coverage_end=data.get("coverage_end", verification.coverage_end),
            )
        cls.validate_amounts(
            copay_amount=data.get("copay_amount", verification.copay_amount),
            deductible_amount=data.get(
                "deductible_amount", verification.deductible_amount
            ),
            coinsurance_percent=data.get(
                "coinsurance_percent",
                verification.coinsurance_percent,
            ),
        )

        if "patient_id" in data:
            cls.validate_patient(
                organization_id=organization_id,
                patient_id=data["patient_id"],
            )

        for field, value in data.items():
            setattr(verification, field, value)
        verification.save()
        return verification

    @classmethod
    @transaction.atomic
    def soft_delete(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        deleted_by_id: UUID | None,
    ) -> InsuranceVerification:
        """Soft-delete a verification under row lock."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        if verification.status == VerificationStatus.IN_PROGRESS.value:
            raise InsuranceVerificationInvariantError(
                "An in-progress verification cannot be deleted."
            )
        verification.soft_delete(user_id=deleted_by_id)
        return verification

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
    ) -> InsuranceVerification:
        """Restore a deleted verification under row lock."""

        verification = get_deleted_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        verification.restore()
        return verification

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        verification_id: UUID,
        target_status: str,
        actor_id: UUID | None,
        outcome: str | None = None,
        response_code: str | None = None,
        response_message: str | None = None,
        response_payload: dict[str, Any] | None = None,
        failure_reason: str | None = None,
    ) -> InsuranceVerification:
        """Apply a strict lifecycle transition atomically."""

        verification = get_verification_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            verification_id=verification_id,
        )
        current = verification.status
        allowed = _ALLOWED_TRANSITIONS.get(current, set())
        if target_status not in allowed:
            raise InsuranceVerificationTransitionError(
                f"Invalid Insurance Verification transition: {current} -> {target_status}."
            )

        verification.status = target_status
        if outcome is not None:
            verification.outcome = outcome
        if response_code is not None:
            verification.response_code = response_code
        if response_message is not None:
            verification.response_message = response_message
        if response_payload is not None:
            verification.response_payload = response_payload
        if failure_reason is not None:
            verification.failure_reason = failure_reason

        if target_status == VerificationStatus.VERIFIED.value:
            verification.verified_at = timezone.now()
            verification.verified_by_id = actor_id
            if verification.outcome == VerificationOutcome.UNKNOWN.value:
                verification.outcome = VerificationOutcome.ACTIVE.value

        verification.save()
        return verification


__all__ = ("InsuranceVerificationService", "_ALLOWED_TRANSITIONS")
