"""
Emergency Contact primary designation domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EmergencyContactPrimaryChangedEvent(DomainEvent):
    """
    Fired when the patient's primary emergency contact changes.
    """

    tenant_id: UUID
    actor_id: UUID
    emergency_contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_primary: bool
    new_primary: bool


__all__ = ("EmergencyContactPrimaryChangedEvent",)
