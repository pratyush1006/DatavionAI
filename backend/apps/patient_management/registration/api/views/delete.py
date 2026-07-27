"""
Delete API view for the Patient Registration module.
"""

from __future__ import annotations

from apps.common.api import (
    BaseDestroyAPIView,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationDeleteAPIView(
    BaseDestroyAPIView,
):
    """
    API view for deleting a registration.
    """

    queryset = PatientRegistration.objects.all()

    lookup_field = "id"
