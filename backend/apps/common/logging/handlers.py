"""
Logging handlers.

Provides reusable logging handler factories for the DatavionAI
observability framework.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from logging.handlers import RotatingFileHandler
from pathlib import Path

from apps.common.logging.filters import (
    HealthCheckFilter,
    RequestContextFilter,
    SensitiveDataFilter,
)
from apps.common.logging.formatters import (
    ConsoleFormatter,
    JSONFormatter,
)


def _apply_filters(
    handler: logging.Handler,
    filters: Iterable[logging.Filter] | None = None,
) -> logging.Handler:
    """
    Apply common logging filters.
    """

    default_filters = (
        RequestContextFilter(),
        SensitiveDataFilter(),
        HealthCheckFilter(),
    )

    for log_filter in filters or default_filters:
        handler.addFilter(
            log_filter,
        )

    return handler


def create_console_handler(
    *,
    level: int = logging.INFO,
    filters: Iterable[logging.Filter] | None = None,
) -> logging.Handler:
    """
    Create a console logging handler.
    """

    handler = logging.StreamHandler()

    handler.setLevel(
        level,
    )

    handler.setFormatter(
        ConsoleFormatter(),
    )

    return _apply_filters(
        handler,
        filters,
    )


def create_json_console_handler(
    *,
    level: int = logging.INFO,
    filters: Iterable[logging.Filter] | None = None,
) -> logging.Handler:
    """
    Create a JSON console logging handler.
    """

    handler = logging.StreamHandler()

    handler.setLevel(
        level,
    )

    handler.setFormatter(
        JSONFormatter(),
    )

    return _apply_filters(
        handler,
        filters,
    )


def create_rotating_file_handler(
    *,
    filename: str | Path,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    encoding: str = "utf-8",
    level: int = logging.INFO,
    filters: Iterable[logging.Filter] | None = None,
) -> logging.Handler:
    """
    Create a rotating JSON file handler.
    """

    path = Path(
        filename,
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    handler = RotatingFileHandler(
        filename=path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )

    handler.setLevel(
        level,
    )

    handler.setFormatter(
        JSONFormatter(),
    )

    return _apply_filters(
        handler,
        filters,
    )


__all__: tuple[str, ...] = (
    "create_console_handler",
    "create_json_console_handler",
    "create_rotating_file_handler",
)
