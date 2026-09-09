"""Patient Preferences serializer exports."""

from __future__ import annotations

from apps.patient_management.preferences.api.serializers.preference import (
    PatientCommunicationPreferenceRequestSerializer,
    PatientCommunicationPreferenceSerializer,
    PatientPreferenceCreateSerializer,
    PatientPreferenceDetailSerializer,
    PatientPreferenceListSerializer,
    PatientPreferenceUpdateSerializer,
)

__all__ = (
    "PatientCommunicationPreferenceRequestSerializer",
    "PatientCommunicationPreferenceSerializer",
    "PatientPreferenceCreateSerializer",
    "PatientPreferenceDetailSerializer",
    "PatientPreferenceListSerializer",
    "PatientPreferenceUpdateSerializer",
)
