"""
API views for the Patient Preferences module.
"""

from .communication_preference import (
    PatientCommunicationPreferenceCreateAPIView,
    PatientCommunicationPreferenceDeleteAPIView,
    PatientCommunicationPreferenceDetailAPIView,
    PatientCommunicationPreferenceListAPIView,
    PatientCommunicationPreferenceUpdateAPIView,
)
from .preference import (
    PatientPreferenceCreateAPIView,
    PatientPreferenceDeleteAPIView,
    PatientPreferenceDetailAPIView,
    PatientPreferenceListAPIView,
    PatientPreferenceUpdateAPIView,
)

__all__ = [
    "PatientCommunicationPreferenceCreateAPIView",
    "PatientCommunicationPreferenceDeleteAPIView",
    "PatientCommunicationPreferenceDetailAPIView",
    "PatientCommunicationPreferenceListAPIView",
    "PatientCommunicationPreferenceUpdateAPIView",
    "PatientPreferenceCreateAPIView",
    "PatientPreferenceDeleteAPIView",
    "PatientPreferenceDetailAPIView",
    "PatientPreferenceListAPIView",
    "PatientPreferenceUpdateAPIView",
]
