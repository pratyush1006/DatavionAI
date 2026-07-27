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
from apps.clinical.patients.selectors import PatientSelector
from apps.clinical.patients.services import PatientService
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)

PATIENT_TAG: Final[tuple[str, ...]] = ("Patients",)


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

    serializer_class = PatientDetailSerializer

    serializer_classes = {
        "GET": PatientDetailSerializer,
        "PUT": PatientUpdateSerializer,
        "PATCH": PatientUpdateSerializer,
    }

    update_service = PatientService.update

    delete_service = PatientService.delete

    def get_object(
        self,
    ) -> Patient:
        """
        Return the requested patient.
        """

        return PatientSelector.get(
            patient_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientRetrieveUpdateDestroyAPIView",
]
