"""
Update API view for the Patient Registration module.
"""

from __future__ import annotations

from apps.common.api import (
    BaseUpdateAPIView,
)
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationUpdateSerializer,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationUpdateAPIView(
    BaseUpdateAPIView,
):
    """
    API view for updating a registration.
    """

    queryset = PatientRegistration.objects.all()

    serializer_class = PatientRegistrationUpdateSerializer

    lookup_field = "id"
