"""
Patient API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.clinical.patients.api.views import (
    PatientListCreateAPIView,
    PatientRetrieveUpdateDestroyAPIView,
)

app_name = "patients"

urlpatterns = [
    path(
        "",
        PatientListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:patient_id>/",
        PatientRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
