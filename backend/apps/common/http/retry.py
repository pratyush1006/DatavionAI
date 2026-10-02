"""
HTTP retry configuration.

Provides reusable retry configuration for the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.http.constants import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_MAX_RETRIES,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RetryConfiguration:
    """
    HTTP retry configuration.
    """

    max_retries: int = DEFAULT_MAX_RETRIES

    backoff_factor: float = DEFAULT_BACKOFF_FACTOR

    retry_status_codes: tuple[int, ...] = (
        408,  # Request Timeout
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    )

    retry_methods: tuple[str, ...] = (
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PUT",
    )

    retry_on_connection_error: bool = True

    retry_on_timeout: bool = True


DEFAULT_RETRY_CONFIGURATION: RetryConfiguration = RetryConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_RETRY_CONFIGURATION",
    "RetryConfiguration",
)
