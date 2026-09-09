"""
Emergency Contact status changed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EmergencyContactStatusChangedEvent(DomainEvent):
    """
    Fired when emergency contact lifecycle status changes.
    """

    tenant_id: UUID
    actor_id: UUID
    emergency_contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("EmergencyContactStatusChangedEvent",)
