"""Patient Preferences permission exports."""

from __future__ import annotations

from apps.patient_management.preferences.permissions.preference import (
    CanCreatePatientPreference,
    CanDeletePatientPreference,
    CanListPatientPreferences,
    CanManageCommunicationPreference,
    CanRestorePatientPreference,
    CanUpdatePatientPreference,
    CanViewPatientPreference,
    PatientPreferencePermission,
)

__all__ = (
    "CanCreatePatientPreference",
    "CanDeletePatientPreference",
    "CanListPatientPreferences",
    "CanManageCommunicationPreference",
    "CanRestorePatientPreference",
    "CanUpdatePatientPreference",
    "CanViewPatientPreference",
    "PatientPreferencePermission",
)
