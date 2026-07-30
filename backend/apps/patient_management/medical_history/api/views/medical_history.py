"""
API views for the Medical History module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.medical_history.api.serializers import (
    PatientMedicalHistoryCreateSerializer,
    PatientMedicalHistoryDetailSerializer,
    PatientMedicalHistoryListSerializer,
    PatientMedicalHistoryUpdateSerializer,
)
from apps.patient_management.medical_history.models import PatientMedicalHistory
from apps.patient_management.medical_history.permissions import (
    CanCreatePatientMedicalHistory,
    CanDeletePatientMedicalHistory,
    CanUpdatePatientMedicalHistory,
    CanViewPatientMedicalHistory,
)
from apps.patient_management.medical_history.selectors import (
    PatientMedicalHistorySelector,
)
from apps.patient_management.medical_history.services import (
    PatientMedicalHistoryService,
)
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Medical History",)


@extend_schema(tags=TAG)
class PatientMedicalHistoryListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientMedicalHistory),
        "POST": (IsAuthenticated, CanCreatePatientMedicalHistory),
    }

    serializer_classes = {
        "GET": PatientMedicalHistoryListSerializer,
        "POST": PatientMedicalHistoryCreateSerializer,
    }

    detail_serializer_class = PatientMedicalHistoryDetailSerializer

    create_service = PatientMedicalHistoryService.create

    create_success_message = "Medical History created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PatientMedicalHistory]:
        return PatientMedicalHistorySelector.queryset()


@extend_schema(tags=TAG)
class PatientMedicalHistoryRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "medical_history_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientMedicalHistory),
        "PUT": (IsAuthenticated, CanUpdatePatientMedicalHistory),
        "PATCH": (IsAuthenticated, CanUpdatePatientMedicalHistory),
        "DELETE": (IsAuthenticated, CanDeletePatientMedicalHistory),
    }

    serializer_classes = {
        "GET": PatientMedicalHistoryDetailSerializer,
        "PUT": PatientMedicalHistoryUpdateSerializer,
        "PATCH": PatientMedicalHistoryUpdateSerializer,
    }

    update_service = PatientMedicalHistoryService.update
    delete_service = PatientMedicalHistoryService.delete

    def get_object(
        self,
    ) -> PatientMedicalHistory:
        return PatientMedicalHistorySelector.get(
            medical_history_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientMedicalHistoryListCreateAPIView",
    "PatientMedicalHistoryRetrieveUpdateDestroyAPIView",
]
