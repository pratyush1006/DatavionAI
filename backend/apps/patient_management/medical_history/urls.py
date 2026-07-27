"""
URL patterns for the Medical History module.
"""

from __future__ import annotations

from apps.patient_management.medical_history.api.views import (
    PatientMedicalHistoryListCreateAPIView,
    PatientMedicalHistoryRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "medical_histories"

urlpatterns = [
    path(
        "",
        PatientMedicalHistoryListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:medical_history_id>/",
        PatientMedicalHistoryRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
