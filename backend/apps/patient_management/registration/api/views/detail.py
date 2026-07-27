"""
Retrieve API view for the Patient Registration module.
"""

from __future__ import annotations

from apps.common.api import (
    BaseRetrieveAPIView,
)
from apps.patient_management.registration.api.serializers import (
    PatientRegistrationDetailSerializer,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationDetailAPIView(
    BaseRetrieveAPIView,
):
    """
    API view for retrieving a registration.
    """

    queryset = PatientRegistration.objects.all()

    serializer_class = PatientRegistrationDetailSerializer

    lookup_field = "id"
