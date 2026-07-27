"""
Framework logger.

Provides the canonical logger factory for the DatavionAI
observability framework.

Application code should obtain loggers exclusively through this
module instead of calling ``logging.getLogger()`` directly.
"""

from __future__ import annotations

import logging

from apps.common.logging.constants import (
    DEFAULT_LOGGER_NAME,
)
from apps.common.logging.handlers import (
    create_json_console_handler,
)


def configure_logger(
    logger: logging.Logger,
    *,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure a logger instance.

    Configuration is idempotent and safe for Django reloads.
    """

    logger.setLevel(
        level,
    )

    logger.propagate = False

    if not logger.handlers:
        handler = create_json_console_handler(
            level=level,
        )

        logger.addHandler(
            handler,
        )

    return logger


def get_logger(
    name: str | None = None,
    *,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name:
            Logger name. If omitted, framework logger is returned.

        level:
            Logger severity level.

    Returns:
        Configured logger instance.
    """

    logger = logging.getLogger(
        name or DEFAULT_LOGGER_NAME,
    )

    return configure_logger(
        logger,
        level=level,
    )


__all__: tuple[str, ...] = (
    "configure_logger",
    "get_logger",
)
