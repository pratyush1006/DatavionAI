"""
URL patterns for the Patient Consents API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.consents.api.views import (
    ConsentCreateAPIView,
    ConsentDeleteAPIView,
    ConsentDetailAPIView,
    ConsentListAPIView,
    ConsentUpdateAPIView,
)

app_name = "consents-api"

urlpatterns = [
    path(
        "",
        ConsentListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        ConsentCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:id>/",
        ConsentDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:id>/update/",
        ConsentUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:id>/delete/",
        ConsentDeleteAPIView.as_view(),
        name="delete",
    ),
]
