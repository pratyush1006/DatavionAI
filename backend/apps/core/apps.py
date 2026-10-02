"""
Core application configuration.
"""

from __future__ import annotations

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    """
    Django application configuration for the DatavionOS Core module.

    Provides foundational platform components:

    - Base models
    - System checks
    - Registries
    - Lifecycle hooks
    - Platform metadata
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.core"

    label = "core"

    verbose_name = "DatavionOS Core"

    def ready(
        self,
    ) -> None:
        """
        Perform lightweight startup initialization.

        Only imports registration modules.
        No database queries, cache calls,
        or network operations allowed.
        """

        # Register Django system checks
        # Register signals
        from apps.core import (
            checks,  # noqa: F401
            signals,  # noqa: F401
        )

        logger.debug(
            "DatavionOS Core application initialized.",
        )


__all__ = [
    "CoreConfig",
]
