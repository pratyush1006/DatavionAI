"""
Serializers for the Patient Registration module.
"""

from apps.patient_management.registration.api.serializers.create import (
    PatientRegistrationCreateSerializer,
)
from apps.patient_management.registration.api.serializers.detail import (
    PatientRegistrationDetailSerializer,
)
from apps.patient_management.registration.api.serializers.list import (
    PatientRegistrationListSerializer,
)
from apps.patient_management.registration.api.serializers.update import (
    PatientRegistrationUpdateSerializer,
)

__all__ = [
    "PatientRegistrationCreateSerializer",
    "PatientRegistrationDetailSerializer",
    "PatientRegistrationListSerializer",
    "PatientRegistrationUpdateSerializer",
]
