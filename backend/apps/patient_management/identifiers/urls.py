"""
URL configuration for the Patient Identifiers module.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.identifiers.api.urls",
        ),
    ),
]


__all__ = ("urlpatterns",)
