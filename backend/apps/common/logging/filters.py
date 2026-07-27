"""
Logging filters.

Provides reusable logging filters for the DatavionAI
observability framework.
"""

from __future__ import annotations

import logging
from typing import Final

from apps.common.logging.context import (
    get_logging_context,
)

SENSITIVE_FIELDS: Final[tuple[str, ...]] = (
    "password",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "authorization",
)


class RequestContextFilter(
    logging.Filter,
):
    """
    Inject request-scoped context into log records.

    Logging failures must never affect application execution.
    """

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """
        Enrich log records with context.
        """

        try:
            context = get_logging_context()

        except Exception:
            context = {}

        for key, value in context.items():
            setattr(
                record,
                key,
                value,
            )

        return True


class SensitiveDataFilter(
    logging.Filter,
):
    """
    Mask sensitive information from logs.

    Protects secrets, credentials, and authentication data.
    """

    MASK = "***REDACTED***"

    def _sanitize(
        self,
        value: object,
    ) -> object:
        """
        Sanitize nested values.
        """

        if isinstance(
            value,
            dict,
        ):
            return {
                key: (
                    self.MASK
                    if key.lower() in SENSITIVE_FIELDS
                    else self._sanitize(value)
                )
                for key, value in value.items()
            }

        if isinstance(
            value,
            list,
        ):
            return [self._sanitize(item) for item in value]

        return value

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """
        Mask sensitive log values.
        """

        if isinstance(
            record.msg,
            dict,
        ):
            record.msg = self._sanitize(
                record.msg,
            )

        return True


class HealthCheckFilter(
    logging.Filter,
):
    """
    Suppress routine health check logs.
    """

    HEALTH_PATHS: Final[tuple[str, ...]] = (
        "/health/",
        "/healthz/",
        "/live/",
        "/ready/",
    )

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """
        Filter health check records.
        """

        path = getattr(
            record,
            "request_path",
            "",
        )

        return not any(path.startswith(prefix) for prefix in self.HEALTH_PATHS)


__all__: tuple[str, ...] = (
    "HealthCheckFilter",
    "RequestContextFilter",
    "SensitiveDataFilter",
)
