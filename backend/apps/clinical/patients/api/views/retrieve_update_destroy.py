"""
API views for retrieving, updating, and deleting patients.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.patients.api.serializers import (
    PatientDetailSerializer,
    PatientUpdateSerializer,
)
from apps.clinical.patients.models import Patient
from apps.clinical.patients.permissions import (
    CanDeletePatient,
    CanUpdatePatient,
    CanViewPatient,
)
from apps.clinical.patients.selectors import get_patient_by_id
from apps.clinical.patients.services import (
    delete_patient,
    update_patient,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

PATIENT_TAG: Final = ("Patients",)


@extend_schema(tags=PATIENT_TAG)
class PatientRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient.
    """

    lookup_url_kwarg = "patient_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPatient,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePatient,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePatient,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePatient,
        ),
    }

    # Default serializer used by DRF, Browsable API and drf-spectacular.
    serializer_class = PatientDetailSerializer

    # Method-specific serializer overrides.
    serializer_classes = {
        "GET": PatientDetailSerializer,
        "PUT": PatientUpdateSerializer,
        "PATCH": PatientUpdateSerializer,
    }

    update_service = update_patient

    delete_service = delete_patient

    def get_object(
        self,
    ) -> Patient:
        """
        Return the requested patient.
        """

        return get_patient_by_id(
            patient_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientRetrieveUpdateDestroyAPIView",
]
