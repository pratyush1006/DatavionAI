"""Patient Preferences API URL patterns."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.preferences.api.views import (
    PatientCommunicationPreferenceAPIView,
    PatientPreferenceDeleteAPIView,
    PatientPreferenceDetailAPIView,
    PatientPreferenceListCreateAPIView,
    PatientPreferenceRestoreAPIView,
)

urlpatterns = [
    path(
        "",
        PatientPreferenceListCreateAPIView.as_view(),
        name="patient-preferences-list-create",
    ),
    path(
        "<uuid:preference_id>/",
        PatientPreferenceDetailAPIView.as_view(),
        name="patient-preferences-detail",
    ),
    path(
        "<uuid:preference_id>/delete/",
        PatientPreferenceDeleteAPIView.as_view(),
        name="patient-preferences-delete",
    ),
    path(
        "<uuid:preference_id>/restore/",
        PatientPreferenceRestoreAPIView.as_view(),
        name="patient-preferences-restore",
    ),
    path(
        "<uuid:preference_id>/communication/",
        PatientCommunicationPreferenceAPIView.as_view(),
        name="patient-preferences-communication",
    ),
]

app_name = "patient_preferences"

__all__ = ("urlpatterns",)
