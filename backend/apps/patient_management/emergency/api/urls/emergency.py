"""URL routes for patient emergency APIs."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.emergency.api.views import (
    EmergencyLifecycleView,
    EmergencyListCreateView,
    EmergencyRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "",
        EmergencyListCreateView.as_view(),
        name="emergency-list-create",
    ),
    path(
        "<uuid:emergency_id>/",
        EmergencyRetrieveUpdateDestroyView.as_view(),
        name="emergency-detail",
    ),
    path(
        "<uuid:emergency_id>/lifecycle/<str:action>/",
        EmergencyLifecycleView.as_view(),
        name="emergency-lifecycle",
    ),
]


__all__ = ("urlpatterns",)
