"""Charge Capture domain events."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

__all__ = (
    "ChargeCapturedEvent",
    "ChargeStatusChangedEvent",
    "ChargeVoidedEvent",
)


@dataclass(frozen=True, slots=True)
class ChargeCapturedEvent:
    """Describe a newly captured charge."""

    charge_id: UUID
    tenant_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True)
class ChargeStatusChangedEvent:
    """Describe a charge lifecycle transition."""

    charge_id: UUID
    tenant_id: UUID
    previous_status: str
    new_status: str


@dataclass(frozen=True, slots=True)
class ChargeVoidedEvent:
    """Describe a charge void operation."""

    charge_id: UUID
    tenant_id: UUID
    reason: str
