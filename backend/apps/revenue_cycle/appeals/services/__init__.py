"""
Revenue Cycle Appeals application services.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.core.events import publisher
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.appeals.constants import (
    ALLOWED_TRANSITIONS,
    AppealStatus,
)
from apps.revenue_cycle.appeals.events import (
    AppealCreated,
    AppealDeleted,
    AppealRestored,
    AppealTransitioned,
)
from apps.revenue_cycle.appeals.exceptions import (
    AppealInvariantError,
    AppealNotFoundError,
    InvalidAppealTransition,
)
from apps.revenue_cycle.appeals.models import Appeal
from apps.revenue_cycle.appeals.selectors import (
    get_appeal_for_update,
    get_deleted_appeal_for_update,
)


def _publish_after_commit(event: Any) -> None:
    """Publish an event only after the surrounding transaction commits."""
    transaction.on_commit(lambda: publisher.publish(event))


class AppealService:
    """Perform transactional Revenue Cycle Appeals mutations."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        actor: Any,
        tenant_id: UUID,
        organization_id: UUID,
        patient_id: UUID,
        data: dict[str, Any],
    ) -> Appeal:
        """Create an appeal in an explicit tenant and organization."""
        organization = Organization.objects.get(
            id=organization_id,
            tenant_id=tenant_id,
        )
        patient = Patient.objects.select_for_update().get(
            id=patient_id,
            organization_id=organization.id,
            is_deleted=False,
        )
        if not patient.is_active:
            raise AppealInvariantError("An inactive patient cannot receive an appeal.")

        idempotency_key = str(data.get("idempotency_key", "")).strip()
        appeal_number = str(data.get("appeal_number", "")).strip()

        if not idempotency_key:
            raise AppealInvariantError("idempotency_key is required.")
        if not appeal_number:
            raise AppealInvariantError("appeal_number is required.")

        existing = Appeal.objects.filter(
            organization_id=organization.id,
            idempotency_key=idempotency_key,
        ).first()
        if existing:
            return existing

        requested_amount = Decimal(str(data.get("requested_amount", "0")))
        approved_amount = Decimal(str(data.get("approved_amount", "0")))
        if requested_amount < 0 or approved_amount < 0:
            raise AppealInvariantError("Appeal amounts cannot be negative.")
        if approved_amount > requested_amount:
            raise AppealInvariantError(
                "approved_amount cannot exceed requested_amount."
            )

        payload = dict(data)
        payload.pop("patient", None)
        payload["organization_id"] = organization.id
        payload["patient_id"] = patient.id
        payload["created_by_id"] = getattr(actor, "id", None)
        payload["updated_by_id"] = getattr(actor, "id", None)

        try:
            appeal = Appeal.objects.create(**payload)
        except IntegrityError:
            appeal = Appeal.objects.get(
                organization_id=organization.id,
                idempotency_key=idempotency_key,
            )
            return appeal

        _publish_after_commit(
            AppealCreated(
                appeal_id=appeal.id,
                organization_id=organization.id,
                patient_id=patient.id,
                claim_reference=appeal.claim_reference,
                tenant_id=tenant_id,
                actor_id=getattr(actor, "id", None),
            )
        )
        return appeal

    @staticmethod
    @transaction.atomic
    def transition(
        *,
        actor: Any,
        tenant_id: UUID,
        organization_id: UUID,
        appeal_id: UUID,
        target_status: str,
        reason: str = "",
    ) -> Appeal:
        """Apply a controlled appeal lifecycle transition."""
        appeal = get_appeal_for_update(
            organization_id=organization_id,
            tenant_id=tenant_id,
            appeal_id=appeal_id,
        )
        if appeal is None:
            raise AppealNotFoundError("Appeal was not found.")

        try:
            target = AppealStatus(target_status)
            current = AppealStatus(appeal.status)
        except ValueError as exc:
            raise InvalidAppealTransition("Unknown appeal lifecycle status.") from exc

        if target not in ALLOWED_TRANSITIONS.get(current, set()):
            raise InvalidAppealTransition(
                f"Cannot transition {current.value} to {target.value}."
            )

        normalized_reason = reason.strip()
        if (
            target
            in {
                AppealStatus.APPROVED,
                AppealStatus.PARTIALLY_APPROVED,
                AppealStatus.DENIED,
            }
            and not normalized_reason
        ):
            raise AppealInvariantError("A decision reason is required.")

        if target == AppealStatus.PARTIALLY_APPROVED:
            if appeal.approved_amount <= 0:
                raise AppealInvariantError(
                    "Partial approval requires an approved amount."
                )
            if appeal.approved_amount >= appeal.requested_amount:
                raise AppealInvariantError(
                    "Partial approval must be less than requested amount."
                )

        previous = appeal.status
        if target == AppealStatus.APPROVED:
            appeal.approved_amount = appeal.requested_amount

        appeal.status = target.value
        appeal.decision_reason = normalized_reason
        if target == AppealStatus.SUBMITTED:
            appeal.submitted_at = timezone.now()
        if target in {
            AppealStatus.APPROVED,
            AppealStatus.PARTIALLY_APPROVED,
            AppealStatus.DENIED,
            AppealStatus.CLOSED,
        }:
            appeal.decided_at = timezone.now()
        appeal.updated_by_id = getattr(actor, "id", None)
        appeal.save()

        _publish_after_commit(
            AppealTransitioned(
                appeal_id=appeal.id,
                organization_id=organization_id,
                from_status=previous,
                to_status=appeal.status,
                tenant_id=tenant_id,
                actor_id=getattr(actor, "id", None),
            )
        )
        return appeal

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        actor: Any,
        tenant_id: UUID,
        organization_id: UUID,
        appeal_id: UUID,
    ) -> Appeal:
        """Soft-delete an appeal under a row lock."""
        appeal = get_appeal_for_update(
            organization_id=organization_id,
            tenant_id=tenant_id,
            appeal_id=appeal_id,
        )
        if appeal is None:
            raise AppealNotFoundError("Appeal was not found.")
        if appeal.status == AppealStatus.CLOSED:
            raise AppealInvariantError("A closed appeal cannot be deleted.")

        appeal.soft_delete(user_id=getattr(actor, "id", None))
        _publish_after_commit(
            AppealDeleted(
                appeal_id=appeal.id,
                organization_id=organization_id,
                tenant_id=tenant_id,
                actor_id=getattr(actor, "id", None),
            )
        )
        return appeal

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        actor: Any,
        tenant_id: UUID,
        organization_id: UUID,
        appeal_id: UUID,
    ) -> Appeal:
        """Restore a deleted appeal under a row lock."""
        appeal = get_deleted_appeal_for_update(
            organization_id=organization_id,
            tenant_id=tenant_id,
            appeal_id=appeal_id,
        )
        if appeal is None:
            raise AppealNotFoundError("Deleted appeal was not found.")

        appeal.restore()
        appeal.updated_by_id = getattr(actor, "id", None)
        appeal.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
                "updated_by",
                "updated_at",
            ]
        )
        _publish_after_commit(
            AppealRestored(
                appeal_id=appeal.id,
                organization_id=organization_id,
                tenant_id=tenant_id,
                actor_id=getattr(actor, "id", None),
            )
        )
        return appeal


__all__ = ("AppealService",)
