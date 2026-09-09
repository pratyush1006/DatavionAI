"""Transactional Prior Authorization domain services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.exceptions import (
    PriorAuthorizationInvariantError,
    PriorAuthorizationTransitionError,
)
from apps.revenue_cycle.prior_authorization.models import PriorAuthorization
from apps.revenue_cycle.prior_authorization.selectors import (
    get_authorization_for_update,
    get_deleted_authorization_for_update,
)

_ALLOWED_TRANSITIONS = {
    AuthorizationStatus.PENDING.value: {
        AuthorizationStatus.IN_REVIEW.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.IN_REVIEW.value: {
        AuthorizationStatus.SUBMITTED.value,
        AuthorizationStatus.APPROVED.value,
        AuthorizationStatus.DENIED.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.SUBMITTED.value: {
        AuthorizationStatus.APPROVED.value,
        AuthorizationStatus.DENIED.value,
        AuthorizationStatus.CANCELLED.value,
    },
    AuthorizationStatus.APPROVED.value: {
        AuthorizationStatus.EXPIRED.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.DENIED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.EXPIRED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.CANCELLED.value: {
        AuthorizationStatus.PENDING.value,
        AuthorizationStatus.INACTIVE.value,
    },
    AuthorizationStatus.INACTIVE.value: set(),
}


class PriorAuthorizationService:
    """Provide transactional mutations for Prior Authorization."""

    @staticmethod
    def validate_request(
        *,
        procedure_code: str,
        requested_units: int | None,
        requested_amount: Decimal | None,
        requested_service_date: date | None,
    ) -> None:
        """Validate the clinical and financial request envelope."""

        if not procedure_code.strip():
            raise PriorAuthorizationInvariantError("procedure_code is required.")
        if requested_units is not None and requested_units <= 0:
            raise PriorAuthorizationInvariantError("requested_units must be positive.")
        if requested_amount is not None and requested_amount < 0:
            raise PriorAuthorizationInvariantError(
                "requested_amount cannot be negative."
            )
        if requested_service_date is not None and requested_service_date < date.today():
            raise PriorAuthorizationInvariantError(
                "requested_service_date cannot be in the past."
            )

    @staticmethod
    def validate_dates(
        *,
        effective_date: date | None,
        expiration_date: date | None,
    ) -> None:
        """Reject an invalid authorization validity interval."""

        if effective_date and expiration_date and expiration_date < effective_date:
            raise PriorAuthorizationInvariantError(
                "expiration_date cannot be earlier than effective_date."
            )

    @staticmethod
    def validate_patient(*, organization_id: UUID, patient_id: UUID) -> None:
        """Ensure the patient belongs to the target organization."""

        patient = Patient.objects.filter(
            pk=patient_id,
            organization_id=organization_id,
        ).first()
        if patient is None:
            raise PriorAuthorizationInvariantError(
                "Patient does not belong to the target organization or is unavailable."
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization_id: UUID,
        patient_id: UUID,
        payer_id: str,
        member_id: str,
        procedure_code: str,
        request_reference: str,
        idempotency_key: str,
        data: dict[str, Any],
    ) -> PriorAuthorization:
        """Create an authorization request idempotently."""

        if not request_reference.strip():
            raise PriorAuthorizationInvariantError("request_reference is required.")
        if not idempotency_key.strip():
            raise PriorAuthorizationInvariantError("idempotency_key is required.")
        if not payer_id.strip() or not member_id.strip():
            raise PriorAuthorizationInvariantError(
                "payer_id and member_id are required."
            )

        cls.validate_patient(
            organization_id=organization_id,
            patient_id=patient_id,
        )
        cls.validate_request(
            procedure_code=procedure_code,
            requested_units=data.get("requested_units"),
            requested_amount=data.get("requested_amount"),
            requested_service_date=data.get("requested_service_date"),
        )
        cls.validate_dates(
            effective_date=data.get("effective_date"),
            expiration_date=data.get("expiration_date"),
        )

        existing = PriorAuthorization.objects.filter(
            organization_id=organization_id,
            idempotency_key=idempotency_key.strip(),
        ).first()
        if existing is not None:
            return existing

        return PriorAuthorization.objects.create(
            organization_id=organization_id,
            patient_id=patient_id,
            payer_id=payer_id.strip(),
            member_id=member_id.strip(),
            procedure_code=procedure_code.strip(),
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
        authorization_id: UUID,
        data: dict[str, Any],
    ) -> PriorAuthorization:
        """Update mutable authorization fields under row lock."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        if authorization.status in {
            AuthorizationStatus.APPROVED.value,
            AuthorizationStatus.EXPIRED.value,
            AuthorizationStatus.INACTIVE.value,
        }:
            protected = {
                "payer_id",
                "member_id",
                "procedure_code",
                "request_reference",
                "idempotency_key",
            }
            if protected.intersection(data):
                raise PriorAuthorizationInvariantError(
                    "Identity fields cannot be changed after a decision."
                )

        cls.validate_request(
            procedure_code=data.get("procedure_code", authorization.procedure_code),
            requested_units=data.get("requested_units", authorization.requested_units),
            requested_amount=data.get(
                "requested_amount", authorization.requested_amount
            ),
            requested_service_date=data.get(
                "requested_service_date",
                authorization.requested_service_date,
            ),
        )
        cls.validate_dates(
            effective_date=data.get("effective_date", authorization.effective_date),
            expiration_date=data.get("expiration_date", authorization.expiration_date),
        )

        if "patient_id" in data:
            cls.validate_patient(
                organization_id=organization_id,
                patient_id=data["patient_id"],
            )

        for field, value in data.items():
            setattr(authorization, field, value)
        authorization.save()
        return authorization

    @classmethod
    @transaction.atomic
    def soft_delete(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
        deleted_by_id: UUID | None,
    ) -> PriorAuthorization:
        """Soft-delete an authorization under row lock."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        if authorization.status in {
            AuthorizationStatus.IN_REVIEW.value,
            AuthorizationStatus.SUBMITTED.value,
        }:
            raise PriorAuthorizationInvariantError(
                "An authorization under active payer review cannot be deleted."
            )
        authorization.soft_delete(user_id=deleted_by_id)
        return authorization

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
    ) -> PriorAuthorization:
        """Restore a deleted authorization under row lock."""

        authorization = get_deleted_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        authorization.restore()
        return authorization

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        authorization_id: UUID,
        target_status: str,
        actor_id: UUID | None,
        outcome: str | None = None,
        response_code: str | None = None,
        response_message: str | None = None,
        response_payload: dict[str, Any] | None = None,
        authorization_number: str | None = None,
        decision_reason: str | None = None,
        effective_date: date | None = None,
        expiration_date: date | None = None,
        approved_units: int | None = None,
        failure_reason: str | None = None,
    ) -> PriorAuthorization:
        """Apply a strict lifecycle transition atomically."""

        authorization = get_authorization_for_update(
            tenant_id=tenant_id,
            organization_id=organization_id,
            authorization_id=authorization_id,
        )
        allowed = _ALLOWED_TRANSITIONS.get(authorization.status, set())
        if target_status not in allowed:
            raise PriorAuthorizationTransitionError(
                f"Invalid Prior Authorization transition: "
                f"{authorization.status} -> {target_status}."
            )

        if effective_date is not None or expiration_date is not None:
            cls.validate_dates(
                effective_date=effective_date or authorization.effective_date,
                expiration_date=expiration_date or authorization.expiration_date,
            )
        if approved_units is not None:
            if approved_units <= 0:
                raise PriorAuthorizationInvariantError(
                    "approved_units must be positive."
                )
            if (
                authorization.requested_units is not None
                and approved_units > authorization.requested_units
            ):
                raise PriorAuthorizationInvariantError(
                    "approved_units cannot exceed requested_units."
                )

        authorization.status = target_status
        if outcome is not None:
            authorization.outcome = outcome
        if response_code is not None:
            authorization.response_code = response_code
        if response_message is not None:
            authorization.response_message = response_message
        if response_payload is not None:
            authorization.response_payload = response_payload
        if authorization_number is not None:
            authorization.authorization_number = authorization_number.strip()
        if decision_reason is not None:
            authorization.decision_reason = decision_reason
        if effective_date is not None:
            authorization.effective_date = effective_date
        if expiration_date is not None:
            authorization.expiration_date = expiration_date
        if approved_units is not None:
            authorization.approved_units = approved_units
        if failure_reason is not None:
            authorization.failure_reason = failure_reason

        if target_status == AuthorizationStatus.SUBMITTED.value:
            authorization.submitted_at = timezone.now()
        if target_status in {
            AuthorizationStatus.APPROVED.value,
            AuthorizationStatus.DENIED.value,
        }:
            authorization.decided_at = timezone.now()
            if target_status == AuthorizationStatus.APPROVED.value:
                authorization.approved_by_id = actor_id
                authorization.outcome = outcome or AuthorizationOutcome.APPROVED.value
            elif outcome is None:
                authorization.outcome = AuthorizationOutcome.DENIED.value

        authorization.save()
        return authorization


__all__ = ("PriorAuthorizationService", "_ALLOWED_TRANSITIONS")
