"""Domain event emitted when an emergency contact is deleted."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EmergencyContactDeleted:
    """Describe an emergency contact deleted event."""

    emergency_id: UUID
    organization_id: UUID
    patient_id: UUID


__all__ = ("EmergencyContactDeleted",)
