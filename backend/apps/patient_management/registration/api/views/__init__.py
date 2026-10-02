"""
API views for the Patient Registration module.
"""

from __future__ import annotations

from apps.patient_management.registration.api.views.lifecycle import (
    PatientRegistrationCancelAPIView,
    PatientRegistrationCheckInAPIView,
    PatientRegistrationCompleteAPIView,
    PatientRegistrationNoShowAPIView,
    PatientRegistrationRejectAPIView,
    PatientRegistrationVerifyAPIView,
)
from apps.patient_management.registration.api.views.list_create import (
    PatientRegistrationListCreateAPIView,
)
from apps.patient_management.registration.api.views.retrieve_update_destroy import (
    PatientRegistrationRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "PatientRegistrationCancelAPIView",
    "PatientRegistrationCheckInAPIView",
    "PatientRegistrationCompleteAPIView",
    "PatientRegistrationListCreateAPIView",
    "PatientRegistrationNoShowAPIView",
    "PatientRegistrationRejectAPIView",
    "PatientRegistrationRetrieveUpdateDestroyAPIView",
    "PatientRegistrationVerifyAPIView",
)
