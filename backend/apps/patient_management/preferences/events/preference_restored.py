"""Patient Preferences domain event."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientPreferenceRestoredEvent(DomainEvent):
    """Represent an immutable Patient Preferences domain event."""

    event_type = "patient_preferences.restored"

    tenant_id: UUID
    actor_id: UUID
    organization_id: UUID
    preference_id: UUID
    patient_id: UUID


__all__ = ("PatientPreferenceRestoredEvent",)
