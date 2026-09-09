"""
Patient Core URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "patients"


urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.patients.api.urls",
        ),
    ),
]


__all__ = (
    "app_name",
    "urlpatterns",
)
