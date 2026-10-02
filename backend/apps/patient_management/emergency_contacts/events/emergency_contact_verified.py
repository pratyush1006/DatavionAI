"""
Emergency Contact verification domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EmergencyContactVerifiedEvent(DomainEvent):
    """
    Fired when an emergency contact becomes verified.
    """

    tenant_id: UUID
    actor_id: UUID
    emergency_contact_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_verified: bool
    new_verified: bool


__all__ = ("EmergencyContactVerifiedEvent",)
