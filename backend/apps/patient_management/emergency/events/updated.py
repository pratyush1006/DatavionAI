"""Domain event emitted when an emergency contact is updated."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EmergencyContactUpdated:
    """Describe an emergency contact updated event."""

    emergency_id: UUID
    organization_id: UUID
    patient_id: UUID


__all__ = ("EmergencyContactUpdated",)
