"""
Views for the Patient Registration module.
"""

from apps.patient_management.registration.api.views.create import (
    PatientRegistrationCreateAPIView,
)
from apps.patient_management.registration.api.views.delete import (
    PatientRegistrationDeleteAPIView,
)
from apps.patient_management.registration.api.views.detail import (
    PatientRegistrationDetailAPIView,
)
from apps.patient_management.registration.api.views.list import (
    PatientRegistrationListAPIView,
)
from apps.patient_management.registration.api.views.update import (
    PatientRegistrationUpdateAPIView,
)

__all__ = [
    "PatientRegistrationCreateAPIView",
    "PatientRegistrationDeleteAPIView",
    "PatientRegistrationDetailAPIView",
    "PatientRegistrationListAPIView",
    "PatientRegistrationUpdateAPIView",
]
