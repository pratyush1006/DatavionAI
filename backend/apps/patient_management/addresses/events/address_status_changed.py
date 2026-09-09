"""
Patient Address status-changed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class AddressStatusChangedEvent(
    DomainEvent,
):
    tenant_id: UUID
    actor_id: UUID
    address_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("AddressStatusChangedEvent",)
