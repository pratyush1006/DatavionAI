"""
URL configuration for the Patient Registration module.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.registration.api.views import (
    PatientRegistrationCreateAPIView,
    PatientRegistrationDeleteAPIView,
    PatientRegistrationDetailAPIView,
    PatientRegistrationListAPIView,
    PatientRegistrationUpdateAPIView,
)

app_name = "registration-api"

urlpatterns = [
    path(
        "",
        PatientRegistrationListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        PatientRegistrationCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:uuid>/",
        PatientRegistrationDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:uuid>/update/",
        PatientRegistrationUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:uuid>/delete/",
        PatientRegistrationDeleteAPIView.as_view(),
        name="delete",
    ),
]
