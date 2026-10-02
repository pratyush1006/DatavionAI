"""
Patient Timeline API URL configuration.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.timeline.api.views import (
    TimelineLifecycleView,
    TimelineListCreateAPIView,
    TimelineRestoreView,
    TimelineRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        TimelineListCreateAPIView.as_view(),
        name="timeline-list-create",
    ),
    path(
        "<uuid:pk>/",
        TimelineRetrieveUpdateDestroyAPIView.as_view(),
        name="timeline-detail",
    ),
    path(
        "<uuid:pk>/lifecycle/",
        TimelineLifecycleView.as_view(),
        name="timeline-lifecycle",
    ),
    path(
        "<uuid:pk>/restore/",
        TimelineRestoreView.as_view(),
        name="timeline-restore",
    ),
]


__all__ = ("urlpatterns",)
