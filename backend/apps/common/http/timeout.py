"""
HTTP timeout configuration.

Provides reusable timeout configuration for the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.http.constants import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_POOL_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_TIMEOUT,
    DEFAULT_WRITE_TIMEOUT,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TimeoutConfiguration:
    """
    HTTP timeout configuration.

    Attributes:
        timeout:
            Overall timeout applied when supported by the
            underlying HTTP client.

        connect:
            Maximum time to establish a connection.

        read:
            Maximum time to wait for a response body.

        write:
            Maximum time to send the request body.

        pool:
            Maximum time to acquire a connection from the
            connection pool.
    """

    timeout: float = DEFAULT_TIMEOUT

    connect: float = DEFAULT_CONNECT_TIMEOUT

    read: float = DEFAULT_READ_TIMEOUT

    write: float = DEFAULT_WRITE_TIMEOUT

    pool: float = DEFAULT_POOL_TIMEOUT


DEFAULT_TIMEOUT_CONFIGURATION: TimeoutConfiguration = TimeoutConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_TIMEOUT_CONFIGURATION",
    "TimeoutConfiguration",
)
