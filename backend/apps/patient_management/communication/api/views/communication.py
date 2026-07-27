"""
API views for the Communication module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.communication.api.serializers import (
    PatientCommunicationCreateSerializer,
    PatientCommunicationDetailSerializer,
    PatientCommunicationListSerializer,
    PatientCommunicationUpdateSerializer,
)
from apps.patient_management.communication.models import PatientCommunication
from apps.patient_management.communication.permissions import (
    CanCreatePatientCommunication,
    CanDeletePatientCommunication,
    CanUpdatePatientCommunication,
    CanViewPatientCommunication,
)
from apps.patient_management.communication.selectors import PatientCommunicationSelector
from apps.patient_management.communication.services import PatientCommunicationService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TAG: Final[tuple[str, ...]] = ("Communication",)


@extend_schema(tags=TAG)
class PatientCommunicationListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientCommunication),
        "POST": (IsAuthenticated, CanCreatePatientCommunication),
    }

    serializer_classes = {
        "GET": PatientCommunicationListSerializer,
        "POST": PatientCommunicationCreateSerializer,
    }

    detail_serializer_class = PatientCommunicationDetailSerializer

    create_service = PatientCommunicationService.create

    create_success_message = "Communication created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PatientCommunication]:
        return PatientCommunicationSelector.queryset()


@extend_schema(tags=TAG)
class PatientCommunicationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "communication_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientCommunication),
        "PUT": (IsAuthenticated, CanUpdatePatientCommunication),
        "PATCH": (IsAuthenticated, CanUpdatePatientCommunication),
        "DELETE": (IsAuthenticated, CanDeletePatientCommunication),
    }

    serializer_classes = {
        "GET": PatientCommunicationDetailSerializer,
        "PUT": PatientCommunicationUpdateSerializer,
        "PATCH": PatientCommunicationUpdateSerializer,
    }

    update_service = PatientCommunicationService.update
    delete_service = PatientCommunicationService.delete

    def get_object(
        self,
    ) -> PatientCommunication:
        return PatientCommunicationSelector.get(
            communication_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientCommunicationListCreateAPIView",
    "PatientCommunicationRetrieveUpdateDestroyAPIView",
]
