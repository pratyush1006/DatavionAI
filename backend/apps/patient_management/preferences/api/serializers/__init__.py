"""
Patient Preference serializers.
"""

from .create import (
    PatientCommunicationPreferenceCreateSerializer,
    PatientPreferenceCreateSerializer,
)
from .detail import (
    PatientCommunicationPreferenceDetailSerializer,
    PatientPreferenceDetailSerializer,
)
from .list import (
    PatientCommunicationPreferenceListSerializer,
    PatientPreferenceListSerializer,
)
from .update import (
    PatientCommunicationPreferenceUpdateSerializer,
    PatientPreferenceUpdateSerializer,
)

__all__ = [
    "PatientCommunicationPreferenceCreateSerializer",
    "PatientCommunicationPreferenceDetailSerializer",
    "PatientCommunicationPreferenceListSerializer",
    "PatientCommunicationPreferenceUpdateSerializer",
    "PatientPreferenceCreateSerializer",
    "PatientPreferenceDetailSerializer",
    "PatientPreferenceListSerializer",
    "PatientPreferenceUpdateSerializer",
]
