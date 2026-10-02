"""Domain event emitted when an emergency contact is created."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EmergencyContactCreated:
    """Describe an emergency contact created event."""

    emergency_id: UUID
    organization_id: UUID
    patient_id: UUID


__all__ = ("EmergencyContactCreated",)
