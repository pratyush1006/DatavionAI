"""
Emergency Contact deleted domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EmergencyContactDeletedEvent(DomainEvent):
    """
    Fired when an emergency contact is deleted.
    """

    tenant_id: UUID
    actor_id: UUID
    emergency_contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    emergency_contact_number: str


__all__ = ("EmergencyContactDeletedEvent",)
