"""
URL patterns for the Timeline Event module.
"""

from __future__ import annotations

from apps.patient_management.timeline.api.views import (
    PatientTimelineEventListCreateAPIView,
    PatientTimelineEventRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "timeline_events"

urlpatterns = [
    path(
        "",
        PatientTimelineEventListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:timeline_event_id>/",
        PatientTimelineEventRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
