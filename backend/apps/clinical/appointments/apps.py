"""Django application configuration for Clinical Appointments."""

from __future__ import annotations

from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Configure the Clinical Appointments Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clinical.appointments"
    label = "appointments"
    verbose_name = "Clinical Appointments"


__all__ = ("AppointmentsConfig",)
