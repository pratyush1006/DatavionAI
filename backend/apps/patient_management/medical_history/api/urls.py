"""Urls."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.medical_history.api.views import (
    MedicalHistoryActivateAPIView,
    MedicalHistoryDeactivateAPIView,
    MedicalHistoryListCreateAPIView,
    MedicalHistoryRestoreAPIView,
    MedicalHistoryRetrieveUpdateDestroyAPIView,
    MedicalHistoryVerifyAPIView,
)

urlpatterns = [
    path(
        "",
        MedicalHistoryListCreateAPIView.as_view(),
        name="medical-history-list-create",
    ),
    path(
        "<uuid:pk>/",
        MedicalHistoryRetrieveUpdateDestroyAPIView.as_view(),
        name="medical-history-detail",
    ),
    path(
        "<uuid:pk>/activate/",
        MedicalHistoryActivateAPIView.as_view(),
        name="medical-history-activate",
    ),
    path(
        "<uuid:pk>/deactivate/",
        MedicalHistoryDeactivateAPIView.as_view(),
        name="medical-history-deactivate",
    ),
    path(
        "<uuid:pk>/restore/",
        MedicalHistoryRestoreAPIView.as_view(),
        name="medical-history-restore",
    ),
    path(
        "<uuid:pk>/verify/",
        MedicalHistoryVerifyAPIView.as_view(),
        name="medical-history-verify",
    ),
]


__all__ = ("urlpatterns",)
