"""
Application configuration for the Master Patient Index module.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MPIConfig(AppConfig):
    """Configuration for the MPI application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.mpi"
    label = "patient_mpi"
    verbose_name = _("Master Patient Index")

    def ready(self) -> None:
        """Register application components."""
        from apps.patient_management.mpi import signals  # noqa: F401
