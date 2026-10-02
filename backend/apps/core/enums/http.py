"""
HTTP-related enumerations for the DatavionOS platform.

Defines standardized HTTP methods, headers and API
communication constants.
"""

from __future__ import annotations

from enum import StrEnum


class HTTPMethod(StrEnum):
    """
    Supported HTTP methods.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class HTTPHeader(StrEnum):
    """
    Common HTTP headers used across DatavionOS APIs.
    """

    # Standard headers

    AUTHORIZATION = "Authorization"

    CONTENT_TYPE = "Content-Type"

    ACCEPT = "Accept"

    USER_AGENT = "User-Agent"

    # Request tracing

    X_REQUEST_ID = "X-Request-ID"

    X_CORRELATION_ID = "X-Correlation-ID"

    # Proxy / gateway

    X_FORWARDED_FOR = "X-Forwarded-For"

    X_FORWARDED_HOST = "X-Forwarded-Host"

    X_FORWARDED_PROTO = "X-Forwarded-Proto"

    # SaaS context

    X_TENANT_ID = "X-Tenant-ID"

    X_ORGANIZATION_ID = "X-Organization-ID"

    # API management

    X_API_VERSION = "X-API-Version"

    X_CLIENT_ID = "X-Client-ID"

    # Reliability

    IDEMPOTENCY_KEY = "Idempotency-Key"


__all__ = [
    "HTTPHeader",
    "HTTPMethod",
]
