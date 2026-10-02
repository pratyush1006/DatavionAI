"""
Patient Management URL configuration.

Patient Management owns patient-facing bounded contexts.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "patient_management"


urlpatterns = [
    path("", include("apps.patient_management.api.urls")),
]


__all__ = (
    "app_name",
    "urlpatterns",
)
