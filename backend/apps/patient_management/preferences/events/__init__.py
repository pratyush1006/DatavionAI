"""Patient Preferences domain event exports."""

from __future__ import annotations

from apps.patient_management.preferences.events.communication_updated import (
    PatientCommunicationPreferenceUpdatedEvent,
)
from apps.patient_management.preferences.events.preference_created import (
    PatientPreferenceCreatedEvent,
)
from apps.patient_management.preferences.events.preference_deleted import (
    PatientPreferenceDeletedEvent,
)
from apps.patient_management.preferences.events.preference_restored import (
    PatientPreferenceRestoredEvent,
)
from apps.patient_management.preferences.events.preference_updated import (
    PatientPreferenceUpdatedEvent,
)

__all__ = (
    "PatientCommunicationPreferenceUpdatedEvent",
    "PatientPreferenceCreatedEvent",
    "PatientPreferenceDeletedEvent",
    "PatientPreferenceRestoredEvent",
    "PatientPreferenceUpdatedEvent",
)
