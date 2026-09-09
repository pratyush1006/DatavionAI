"""
Patient Management URL configuration.

Patient Management owns patient-facing bounded contexts.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "patient_management"


urlpatterns = [
    path(
        "patients/",
        include(
            "apps.patient_management.patients.urls",
        ),
    ),
    path(
        "profiles/",
        include(
            "apps.patient_management.profile.urls",
        ),
    ),
    path(
        "identifiers/",
        include(
            "apps.patient_management.identifiers.urls",
        ),
    ),
]


__all__ = (
    "app_name",
    "urlpatterns",
)
