"""
Audit application configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class AuditConfig(
    AppConfig,
):
    """
    DatavionOS Audit configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.audit"

    verbose_name = "Audit"

    def ready(
        self,
    ):
        """
        Register audit signals.
        """

        from apps.platform.audit import signals  # noqa: F401
