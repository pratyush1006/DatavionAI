"""
Platform shutdown lifecycle.
"""

from __future__ import annotations

import logging

from apps.core.signals import (
    application_stopping,
)

logger = logging.getLogger(__name__)


def shutdown_platform() -> None:
    """
    Execute graceful DatavionOS shutdown lifecycle.

    Resource cleanup should be handled by registered
    providers listening to application_stopping.
    """

    logger.info(
        "Stopping DatavionOS platform.",
    )

    try:
        application_stopping.send(
            sender=None,
        )

    except Exception:
        logger.exception(
            "DatavionOS shutdown cleanup failed.",
        )
        raise

    logger.info(
        "DatavionOS platform stopped.",
    )


__all__ = [
    "shutdown_platform",
]
