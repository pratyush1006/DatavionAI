"""Clinical Appointment URL entry point."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.clinical.appointments.api.urls"),
    ),
]


__all__ = ("urlpatterns",)
