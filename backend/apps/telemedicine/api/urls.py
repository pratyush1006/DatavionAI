"""
Telemedicine API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.telemedicine.api.views import (
    TelemedicineSessionBulkCreateAPIView,
    TelemedicineSessionEndAPIView,
    TelemedicineSessionListCreateAPIView,
    TelemedicineSessionRetrieveUpdateDestroyAPIView,
    TelemedicineSessionStartAPIView,
)

app_name = "telemedicine"

urlpatterns = [
    path(
        "sessions/",
        TelemedicineSessionListCreateAPIView.as_view(),
        name="session-list-create",
    ),
    path(
        "sessions/<uuid:session_id>/",
        TelemedicineSessionRetrieveUpdateDestroyAPIView.as_view(),
        name="session-detail",
    ),
    path(
        "sessions/<uuid:session_id>/start/",
        TelemedicineSessionStartAPIView.as_view(),
        name="session-start",
    ),
    path(
        "sessions/<uuid:session_id>/end/",
        TelemedicineSessionEndAPIView.as_view(),
        name="session-end",
    ),
    path(
        "sessions/bulk/",
        TelemedicineSessionBulkCreateAPIView.as_view(),
        name="session-bulk-create",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
