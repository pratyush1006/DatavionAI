"""
URLs for PatientPreference.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.preferences.api.views import (
    PatientPreferenceCreateAPIView,
    PatientPreferenceDeleteAPIView,
    PatientPreferenceDetailAPIView,
    PatientPreferenceListAPIView,
    PatientPreferenceUpdateAPIView,
)

urlpatterns = [
    path(
        "",
        PatientPreferenceListAPIView.as_view(),
        name="patient-preference-list",
    ),
    path(
        "create/",
        PatientPreferenceCreateAPIView.as_view(),
        name="patient-preference-create",
    ),
    path(
        "<uuid:uuid>/",
        PatientPreferenceDetailAPIView.as_view(),
        name="patient-preference-detail",
    ),
    path(
        "<uuid:uuid>/update/",
        PatientPreferenceUpdateAPIView.as_view(),
        name="patient-preference-update",
    ),
    path(
        "<uuid:uuid>/delete/",
        PatientPreferenceDeleteAPIView.as_view(),
        name="patient-preference-delete",
    ),
]
