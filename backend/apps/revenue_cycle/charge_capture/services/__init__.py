"""Application services for Charge Capture."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from ..constants import ChargeStatus
from ..events import ChargeCapturedEvent, ChargeStatusChangedEvent, ChargeVoidedEvent
from ..exceptions import ChargeValidationError
from ..models import Charge

__all__ = ("ChargeCaptureService",)


class ChargeCaptureService:
    """Execute transactional Charge Capture mutations."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        actor,
        tenant_id: UUID,
        organization,
        patient,
        service_code: str,
        description: str,
        quantity: Decimal,
        unit_price: Decimal,
        idempotency_key: str | None = None,
    ) -> Charge:
        """Create a charge while enforcing monetary invariants."""

        if idempotency_key:
            existing = Charge.all_objects.filter(
                tenant_id=tenant_id,
                organization=organization,
                idempotency_key=idempotency_key,
            ).first()
            if existing is not None:
                return existing

        total_amount = (quantity * unit_price).quantize(Decimal("0.01"))

        if quantity <= 0:
            raise ChargeValidationError("quantity must be greater than zero.")

        if unit_price < 0:
            raise ChargeValidationError("unit_price cannot be negative.")

        charge = Charge.objects.create(
            patient=patient,
            organization=organization,
            tenant_id=tenant_id,
            service_code=service_code.strip(),
            description=description.strip(),
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            status=ChargeStatus.DRAFT.value,
            idempotency_key=idempotency_key,
        )

        ChargeCaptureService._publish_after_commit(
            ChargeCapturedEvent(
                charge_id=charge.id,
                tenant_id=tenant_id,
                organization_id=organization.id,
                patient_id=patient.id,
            )
        )
        return charge

    @staticmethod
    @transaction.atomic
    def transition(
        *,
        actor,
        tenant_id: UUID,
        organization,
        charge_id: UUID,
        target_status: str,
    ) -> Charge:
        """Transition a charge to a valid lifecycle state."""

        charge = Charge.objects.select_for_update().get(
            id=charge_id,
            tenant_id=tenant_id,
            organization=organization,
            is_deleted=False,
        )
        previous_status = charge.status
        allowed = {
            ChargeStatus.DRAFT.value: {
                ChargeStatus.READY.value,
                ChargeStatus.VOIDED.value,
            },
            ChargeStatus.READY.value: {
                ChargeStatus.SUBMITTED.value,
                ChargeStatus.VOIDED.value,
            },
            ChargeStatus.SUBMITTED.value: set(),
            ChargeStatus.VOIDED.value: set(),
        }

        if target_status not in allowed.get(previous_status, set()):
            raise ChargeValidationError(
                f"Invalid charge transition: {previous_status} -> {target_status}."
            )

        charge.status = target_status
        if target_status == ChargeStatus.READY.value:
            charge.captured_at = timezone.now()
        if target_status == ChargeStatus.VOIDED.value:
            charge.voided_at = timezone.now()

        charge.save(
            update_fields=[
                "status",
                "captured_at",
                "voided_at",
                "updated_at",
            ]
        )

        ChargeCaptureService._publish_after_commit(
            ChargeStatusChangedEvent(
                charge_id=charge.id,
                tenant_id=tenant_id,
                previous_status=previous_status,
                new_status=target_status,
            )
        )
        return charge

    @staticmethod
    @transaction.atomic
    def void(
        *,
        actor,
        tenant_id: UUID,
        organization,
        charge_id: UUID,
        reason: str,
    ) -> Charge:
        """Void a charge through the lifecycle transition service."""

        charge = Charge.objects.select_for_update().get(
            id=charge_id,
            tenant_id=tenant_id,
            organization=organization,
            is_deleted=False,
        )

        if charge.status == ChargeStatus.VOIDED.value:
            return charge

        if charge.status == ChargeStatus.SUBMITTED.value:
            raise ChargeValidationError(
                "Submitted charges cannot be voided by Charge Capture."
            )

        charge.status = ChargeStatus.VOIDED.value
        charge.voided_at = timezone.now()
        charge.void_reason = reason.strip()

        charge.save(
            update_fields=[
                "status",
                "voided_at",
                "void_reason",
                "updated_at",
            ]
        )

        ChargeCaptureService._publish_after_commit(
            ChargeVoidedEvent(
                charge_id=charge.id,
                tenant_id=tenant_id,
                reason=charge.void_reason,
            )
        )
        return charge

    @staticmethod
    def _publish_after_commit(event) -> None:
        """Publish a domain event after the surrounding transaction commits."""

        try:
            from apps.core.events import publisher
        except ImportError:
            return

        transaction.on_commit(lambda: publisher.publish(event))
