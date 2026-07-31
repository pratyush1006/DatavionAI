"""
Common application configuration.

Provides shared framework infrastructure
for the DatavionOS platform.
"""

from __future__ import annotations

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CommonConfig(AppConfig):
    """
    Application configuration for shared
    DatavionOS framework components.

    Responsibilities:

    - API infrastructure
    - Exception handling
    - Event utilities
    - Notification framework
    - Middleware utilities
    - Shared validators
    - Cross-cutting helpers

    Non-responsibilities:

    - Business domains
    - Platform capabilities
    - Audit persistence
    - Tenant services
    - Billing
    - Clinical workflows
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
        # Event Framework Registration
        # --------------------------------------------------------------

        from apps.common import events  # noqa: F401

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
