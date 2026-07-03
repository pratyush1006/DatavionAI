"""
API views for retrieving, updating, and deleting patients.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patients.api.serializers import (
    PatientDetailSerializer,
    PatientUpdateSerializer,
)
from apps.patients.models import Patient
from apps.patients.permissions import (
    CanDeletePatient,
    CanUpdatePatient,
    CanViewPatient,
)
from apps.patients.selectors import get_patient_by_id
from apps.patients.services import (
    delete_patient,
    update_patient,
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

    serializer_classes = {
        "GET": PatientDetailSerializer,
        "PUT": PatientUpdateSerializer,
        "PATCH": PatientUpdateSerializer,
    }

    detail_serializer_class = PatientDetailSerializer

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
