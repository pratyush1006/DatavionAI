"""
Platform startup lifecycle.
"""

from __future__ import annotations

import logging

from apps.core.lifecycle.bootstrap import (
    bootstrap_platform,
)
from apps.core.signals import (
    application_started,
)

logger = logging.getLogger(__name__)


def startup_platform() -> None:
    """
    Execute DatavionOS startup lifecycle.

    Bootstrap must complete successfully before emitting
    the application_started signal.
    """

    logger.info(
        "Starting DatavionOS platform.",
    )

    try:
        bootstrap_platform()

    except Exception:
        logger.exception(
            "DatavionOS startup failed.",
        )
        raise

    application_started.send(
        sender=None,
    )

    logger.info(
        "DatavionOS platform startup completed.",
    )


__all__ = [
    "startup_platform",
]
