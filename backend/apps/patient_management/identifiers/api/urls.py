"""
URL configuration for the Patient Identifiers API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.identifiers.api.views import (
    PatientIdentifierCreateAPIView,
    PatientIdentifierDestroyAPIView,
    PatientIdentifierListAPIView,
    PatientIdentifierRetrieveAPIView,
    PatientIdentifierUpdateAPIView,
)

app_name = "patient-identifiers"

urlpatterns = [
    path(
        "",
        PatientIdentifierListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        PatientIdentifierCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        PatientIdentifierRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        PatientIdentifierUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        PatientIdentifierDestroyAPIView.as_view(),
        name="delete",
    ),
]
