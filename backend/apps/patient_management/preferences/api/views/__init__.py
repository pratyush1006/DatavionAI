"""Patient Preferences API view exports."""

from __future__ import annotations

from apps.patient_management.preferences.api.views.preference import (
    PatientCommunicationPreferenceAPIView,
    PatientPreferenceDeleteAPIView,
    PatientPreferenceDetailAPIView,
    PatientPreferenceListCreateAPIView,
    PatientPreferenceRestoreAPIView,
)

__all__ = (
    "PatientCommunicationPreferenceAPIView",
    "PatientPreferenceDeleteAPIView",
    "PatientPreferenceDetailAPIView",
    "PatientPreferenceListCreateAPIView",
    "PatientPreferenceRestoreAPIView",
)
