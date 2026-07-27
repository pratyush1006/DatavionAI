"""
Common application configuration.

Provides shared infrastructure components for the
DatavionOS platform.
"""

from __future__ import annotations

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CommonConfig(AppConfig):
    """
    Application configuration for the shared Common module.

    Hosts reusable platform infrastructure:

    - API helpers
    - Audit framework
    - Event framework
    - Workflow engine
    - Notification framework
    - Shared services
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.common"

    label = "common"

    verbose_name = "DatavionOS Common"

    def ready(
        self,
    ) -> None:
        """
        Register framework integrations.

        Startup must remain lightweight.

        No:
            - database queries
            - cache calls
            - network calls
            - background workers
        """

        # --------------------------------------------------------------
        # Framework Registrations
        # --------------------------------------------------------------

        from apps.common import (
            audit,  # noqa: F401
            events,  # noqa: F401
            workflow,  # noqa: F401
        )

        # --------------------------------------------------------------
        # Notification Framework Registration
        # --------------------------------------------------------------
        from apps.common.notifications.bootstrap import (
            register_notification_channels,
        )

        register_notification_channels()

        logger.debug(
            "DatavionOS Common initialized.",
        )


__all__ = [
    "CommonConfig",
]
