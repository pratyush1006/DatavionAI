"""
Diagnosis API URLs.
"""

from django.urls import path

from apps.clinical.diagnoses.api.views import (
    DiagnosisListCreateAPIView,
    DiagnosisRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        DiagnosisListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:diagnosis_id>/",
        DiagnosisRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
