"""Patient Preferences model exports."""

from __future__ import annotations

from apps.patient_management.preferences.models.communication_preference import (
    PatientCommunicationPreference,
)
from apps.patient_management.preferences.models.preference import (
    PatientPreference,
)

__all__ = (
    "PatientCommunicationPreference",
    "PatientPreference",
)
