"""
API views for listing and creating patients.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.patients.api.serializers import (
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientListSerializer,
)
from apps.clinical.patients.models import Patient
from apps.clinical.patients.permissions import (
    CanCreatePatient,
    CanViewPatient,
)
from apps.clinical.patients.selectors import get_patients
from apps.clinical.patients.services import create_patient
from apps.common.api.base_generics import BaseListCreateAPIView

PATIENT_TAG: Final[tuple[str, ...]] = ("Patients",)


@extend_schema(tags=PATIENT_TAG)
class PatientListCreateAPIView(BaseListCreateAPIView):
    """
    List existing patients or create a new patient.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPatient,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePatient,
        ),
    }

    serializer_classes = {
        "GET": PatientListSerializer,
        "POST": PatientCreateSerializer,
    }

    detail_serializer_class = PatientDetailSerializer

    create_service = create_patient

    create_success_message = "Patient created successfully."

    search_fields = (
        "mrn",
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    ordering = (
        "first_name",
        "last_name",
    )

    ordering_fields = (
        "mrn",
        "first_name",
        "last_name",
        "created_at",
    )

    filterset_fields = (
        "gender",
        "blood_group",
        "status",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Patient]:
        """
        Return the patients queryset.
        """

        return get_patients()


__all__ = [
    "PatientListCreateAPIView",
]
