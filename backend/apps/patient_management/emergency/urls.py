"""Patient emergency URL entry point."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.patient_management.emergency.api.urls"),
    ),
]


__all__ = ("urlpatterns",)
