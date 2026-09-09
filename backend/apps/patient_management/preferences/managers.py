"""Manager exports for Patient Preferences."""

from __future__ import annotations

from apps.patient_management.preferences.models.communication_preference import (
    PatientCommunicationPreference,
)
from apps.patient_management.preferences.models.preference import (
    PatientPreference,
)

PatientCommunicationPreferenceManager = (
    PatientCommunicationPreference._meta.default_manager.__class__
)
PatientPreferenceManager = PatientPreference._meta.default_manager.__class__

__all__ = (
    "PatientCommunicationPreferenceManager",
    "PatientPreferenceManager",
)
