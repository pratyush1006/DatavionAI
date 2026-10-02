"""
Patient API routes.

Includes:

- Patient CRUD
- Patient lifecycle workflows
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.patients.api.views import (
    PatientActivateAPIView,
    PatientArchiveAPIView,
    PatientDeactivateAPIView,
    PatientListCreateAPIView,
    PatientRestoreAPIView,
    PatientRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # ========================================================
    # CRUD
    # ========================================================
    path(
        "",
        PatientListCreateAPIView.as_view(),
        name="patient-list-create",
    ),
    path(
        "<uuid:patient_id>/",
        PatientRetrieveUpdateDestroyAPIView.as_view(),
        name="patient-detail",
    ),
    # ========================================================
    # Lifecycle
    # ========================================================
    path(
        "<uuid:patient_id>/activate/",
        PatientActivateAPIView.as_view(),
        name="patient-activate",
    ),
    path(
        "<uuid:patient_id>/deactivate/",
        PatientDeactivateAPIView.as_view(),
        name="patient-deactivate",
    ),
    path(
        "<uuid:patient_id>/archive/",
        PatientArchiveAPIView.as_view(),
        name="patient-archive",
    ),
    path(
        "<uuid:patient_id>/restore/",
        PatientRestoreAPIView.as_view(),
        name="patient-restore",
    ),
]


__all__ = ("urlpatterns",)
