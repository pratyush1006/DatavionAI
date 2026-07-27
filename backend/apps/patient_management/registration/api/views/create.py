"""
Create API view for the Patient Registration module.
"""

from __future__ import annotations

from apps.common.api import BaseCreateAPIView
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationCreateSerializer,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationCreateAPIView(
    BaseCreateAPIView,
):
    """
    API view for creating a patient registration.
    """

    queryset = PatientRegistration.objects.all()

    serializer_class = PatientRegistrationCreateSerializer
