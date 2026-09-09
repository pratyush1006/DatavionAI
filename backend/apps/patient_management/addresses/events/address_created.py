"""
Patient Address created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class AddressCreatedEvent(
    DomainEvent,
):
    tenant_id: UUID
    actor_id: UUID
    address_id: UUID
    patient_id: UUID
    organization_id: UUID
    address_type: str
    status: str


__all__ = ("AddressCreatedEvent",)
