"""
API views for the Timeline Event module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.timeline.api.serializers import (
    PatientTimelineEventCreateSerializer,
    PatientTimelineEventDetailSerializer,
    PatientTimelineEventListSerializer,
    PatientTimelineEventUpdateSerializer,
)
from apps.patient_management.timeline.models import PatientTimelineEvent
from apps.patient_management.timeline.permissions import (
    CanCreatePatientTimelineEvent,
    CanDeletePatientTimelineEvent,
    CanUpdatePatientTimelineEvent,
    CanViewPatientTimelineEvent,
)
from apps.patient_management.timeline.selectors import PatientTimelineEventSelector
from apps.patient_management.timeline.services import PatientTimelineEventService

TAG: Final[tuple[str, ...]] = ("Timeline",)


@extend_schema(tags=TAG)
class PatientTimelineEventListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientTimelineEvent),
        "POST": (IsAuthenticated, CanCreatePatientTimelineEvent),
    }

    serializer_classes = {
        "GET": PatientTimelineEventListSerializer,
        "POST": PatientTimelineEventCreateSerializer,
    }

    detail_serializer_class = PatientTimelineEventDetailSerializer

    create_service = PatientTimelineEventService.create

    create_success_message = "Timeline Event created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PatientTimelineEvent]:
        return PatientTimelineEventSelector.queryset()


@extend_schema(tags=TAG)
class PatientTimelineEventRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "timeline_event_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientTimelineEvent),
        "PUT": (IsAuthenticated, CanUpdatePatientTimelineEvent),
        "PATCH": (IsAuthenticated, CanUpdatePatientTimelineEvent),
        "DELETE": (IsAuthenticated, CanDeletePatientTimelineEvent),
    }

    serializer_classes = {
        "GET": PatientTimelineEventDetailSerializer,
        "PUT": PatientTimelineEventUpdateSerializer,
        "PATCH": PatientTimelineEventUpdateSerializer,
    }

    update_service = PatientTimelineEventService.update
    delete_service = PatientTimelineEventService.delete

    def get_object(
        self,
    ) -> PatientTimelineEvent:
        return PatientTimelineEventSelector.get(
            timeline_event_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientTimelineEventListCreateAPIView",
    "PatientTimelineEventRetrieveUpdateDestroyAPIView",
]
