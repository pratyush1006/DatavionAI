"""
URL configuration for the Patient Consents API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.consents.api.views import (
    ConsentCreateAPIView,
    ConsentDestroyAPIView,
    ConsentListAPIView,
    ConsentRetrieveAPIView,
    ConsentUpdateAPIView,
)

app_name = "patient-consents"

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
        "<uuid:pk>/",
        ConsentRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        ConsentUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        ConsentDestroyAPIView.as_view(),
        name="delete",
    ),
]
