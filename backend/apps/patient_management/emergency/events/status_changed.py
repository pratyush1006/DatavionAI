"""Domain event emitted when an emergency contact is status changed."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EmergencyContactStatusChanged:
    """Describe an emergency contact status changed event."""

    emergency_id: UUID
    organization_id: UUID
    patient_id: UUID


__all__ = ("EmergencyContactStatusChanged",)
