"""
Patient API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.clinical.patients.api.views import (
    PatientBulkCreateAPIView,
    PatientBulkDeleteAPIView,
    PatientBulkUpdateAPIView,
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
    path(
        "bulk/",
        PatientBulkCreateAPIView.as_view(),
        name="bulk-create",
    ),
    path(
        "bulk/update/",
        PatientBulkUpdateAPIView.as_view(),
        name="bulk-update",
    ),
    path(
        "bulk/delete/",
        PatientBulkDeleteAPIView.as_view(),
        name="bulk-delete",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
