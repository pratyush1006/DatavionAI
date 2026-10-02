"""Patient Preferences selector exports."""

from __future__ import annotations

from apps.patient_management.preferences.selectors.communication_preference import (
    PatientCommunicationPreferenceSelector,
)
from apps.patient_management.preferences.selectors.preference import (
    PatientPreferenceSelector,
)

__all__ = (
    "PatientCommunicationPreferenceSelector",
    "PatientPreferenceSelector",
)
