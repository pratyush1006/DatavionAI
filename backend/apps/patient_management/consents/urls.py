"""
Top-level URL configuration for Patient Consents.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "apps.patient_management.consents.api.urls",
        ),
    ),
]

__all__ = ("urlpatterns",)
