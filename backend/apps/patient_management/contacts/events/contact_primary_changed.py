"""
Domain event emitted when a patient's primary contact changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class ContactPrimaryChangedEvent(DomainEvent):
    tenant_id: UUID
    actor_id: UUID
    contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    contact_type: str
    previous_primary: bool
    new_primary: bool


__all__ = ("ContactPrimaryChangedEvent",)
