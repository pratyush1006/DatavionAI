"""
Patient Address primary-state domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class AddressPrimaryChangedEvent(
    DomainEvent,
):
    tenant_id: UUID
    actor_id: UUID
    address_id: UUID
    patient_id: UUID
    organization_id: UUID
    address_type: str
    previous_primary: bool
    new_primary: bool


__all__ = ("AddressPrimaryChangedEvent",)
