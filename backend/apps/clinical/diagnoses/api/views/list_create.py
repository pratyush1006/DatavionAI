"""
API views for listing and creating diagnoses.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.diagnoses.api.serializers import (
    DiagnosisCreateSerializer,
    DiagnosisDetailSerializer,
    DiagnosisListSerializer,
)
from apps.clinical.diagnoses.models import Diagnosis
from apps.clinical.diagnoses.permissions import (
    CanCreateDiagnosis,
    CanViewDiagnosis,
)
from apps.clinical.diagnoses.selectors import (
    get_diagnoses,
)
from apps.clinical.diagnoses.services import (
    create_diagnosis,
)
from apps.common.api.base_generics import BaseListCreateAPIView

DIAGNOSIS_TAG: Final[tuple[str, ...]] = ("Diagnoses",)


@extend_schema(tags=DIAGNOSIS_TAG)
class DiagnosisListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing diagnoses or create a new diagnosis.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewDiagnosis,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateDiagnosis,
        ),
    }

    serializer_classes = {
        "GET": DiagnosisListSerializer,
        "POST": DiagnosisCreateSerializer,
    }

    detail_serializer_class = DiagnosisDetailSerializer

    create_service = create_diagnosis

    create_success_message = "Diagnosis created successfully."

    search_fields = (
        "diagnosis_code",
        "diagnosis_description",
        "encounter__encounter_number",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "diagnosis_code",
        "diagnosis_type",
        "status",
        "created_at",
    )

    filterset_fields = (
        "diagnosis_type",
        "status",
        "is_primary",
        "present_on_admission",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Diagnosis]:
        """
        Return the diagnoses queryset.
        """

        return get_diagnoses()


__all__ = [
    "DiagnosisListCreateAPIView",
]
