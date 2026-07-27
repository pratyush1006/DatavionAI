"""
HTTP client configuration.

Provides immutable configuration models shared across the
DatavionAI HTTP framework.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.http.auth import (
    AuthenticationStrategy,
    NoAuthentication,
)
from apps.common.http.retry import (
    DEFAULT_RETRY_CONFIGURATION,
    RetryConfiguration,
)
from apps.common.http.timeout import (
    DEFAULT_TIMEOUT_CONFIGURATION,
    TimeoutConfiguration,
)
from apps.common.http.types import (
    Headers,
    QueryParameters,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RequestOptions:
    """
    Per-request configuration.
    """

    headers: Headers | None = None

    query_params: QueryParameters | None = None

    authentication: AuthenticationStrategy = NoAuthentication()

    timeout: TimeoutConfiguration = DEFAULT_TIMEOUT_CONFIGURATION

    retry: RetryConfiguration = DEFAULT_RETRY_CONFIGURATION

    follow_redirects: bool = True

    verify_ssl: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class ClientConfiguration:
    """
    HTTP client configuration.
    """

    base_url: str = ""

    default_headers: Headers | None = None

    timeout: TimeoutConfiguration = DEFAULT_TIMEOUT_CONFIGURATION

    retry: RetryConfiguration = DEFAULT_RETRY_CONFIGURATION

    authentication: AuthenticationStrategy = NoAuthentication()

    follow_redirects: bool = True

    verify_ssl: bool = True

    http2: bool = True


DEFAULT_CLIENT_CONFIGURATION: ClientConfiguration = ClientConfiguration()

DEFAULT_REQUEST_OPTIONS: RequestOptions = RequestOptions()


__all__: tuple[str, ...] = (
    "ClientConfiguration",
    "DEFAULT_CLIENT_CONFIGURATION",
    "DEFAULT_REQUEST_OPTIONS",
    "RequestOptions",
)
