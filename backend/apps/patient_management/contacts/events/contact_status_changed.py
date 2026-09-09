"""
Domain event emitted when a patient contact status changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class ContactStatusChangedEvent(DomainEvent):
    tenant_id: UUID
    actor_id: UUID
    contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("ContactStatusChangedEvent",)
