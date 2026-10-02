"""Patient Management Registration URL configuration."""

from __future__ import annotations

from django.urls import include, path

app_name = "registration"

urlpatterns = [
    path("", include("apps.patient_management.registration.api.urls")),
]

__all__ = ("app_name", "urlpatterns")
