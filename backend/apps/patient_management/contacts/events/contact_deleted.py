"""
Domain event emitted when a patient contact is deleted.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class ContactDeletedEvent(DomainEvent):
    tenant_id: UUID
    actor_id: UUID
    contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    contact_type: str
    purpose: str


__all__ = ("ContactDeletedEvent",)
