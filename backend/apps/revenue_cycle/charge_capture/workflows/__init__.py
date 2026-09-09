"""Workflow orchestration for Charge Capture."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from ..services import ChargeCaptureService

__all__ = (
    "ChargeCreateWorkflow",
    "ChargeTransitionWorkflow",
    "ChargeVoidWorkflow",
)


class ChargeCreateWorkflow:
    """Orchestrate creation of a revenue-cycle charge."""

    def execute(
        self,
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
    ):
        """Create a charge through the domain service."""

        return ChargeCaptureService.create(
            actor=actor,
            tenant_id=tenant_id,
            organization=organization,
            patient=patient,
            service_code=service_code,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            idempotency_key=idempotency_key,
        )


class ChargeTransitionWorkflow:
    """Orchestrate charge lifecycle transitions."""

    def execute(
        self,
        *,
        actor,
        tenant_id: UUID,
        organization,
        charge_id: UUID,
        target_status: str,
    ):
        """Transition a charge through the domain service."""

        return ChargeCaptureService.transition(
            actor=actor,
            tenant_id=tenant_id,
            organization=organization,
            charge_id=charge_id,
            target_status=target_status,
        )


class ChargeVoidWorkflow:
    """Orchestrate charge voiding."""

    def execute(
        self,
        *,
        actor,
        tenant_id: UUID,
        organization,
        charge_id: UUID,
        reason: str,
    ):
        """Void a charge through the domain service."""

        return ChargeCaptureService.void(
            actor=actor,
            tenant_id=tenant_id,
            organization=organization,
            charge_id=charge_id,
            reason=reason,
        )
