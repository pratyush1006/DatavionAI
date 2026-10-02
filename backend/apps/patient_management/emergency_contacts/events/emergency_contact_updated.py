"""
Emergency Contact updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EmergencyContactUpdatedEvent(DomainEvent):
    """
    Fired when an emergency contact is updated.
    """

    tenant_id: UUID
    actor_id: UUID
    emergency_contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    relationship: str
    status: str
    is_primary: bool


__all__ = ("EmergencyContactUpdatedEvent",)
