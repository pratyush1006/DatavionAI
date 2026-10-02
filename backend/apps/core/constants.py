"""
Core application constants.

Defines immutable platform-wide constants shared across
the DatavionOS kernel.

Only framework-level constants belong here.

Business-specific constants must remain inside their
respective applications.
"""

from __future__ import annotations

from typing import Final

from apps.core.version import (
    API_VERSION,
    PLATFORM_NAME,
    VERSION,
)

# ============================================================================
# Application Identity
# ============================================================================

APP_NAME: Final[str] = PLATFORM_NAME

APP_VERSION: Final[str] = VERSION


# ============================================================================
# Runtime
# ============================================================================

DEFAULT_TIME_ZONE: Final[str] = "UTC"

DEFAULT_CHARSET: Final[str] = "utf-8"

MINIMUM_PYTHON_VERSION: Final[tuple[int, int]] = (
    3,
    12,
)


# ============================================================================
# API
# ============================================================================

DEFAULT_API_VERSION: Final[str] = API_VERSION

DEFAULT_PAGE_SIZE: Final[int] = 20

MAX_PAGE_SIZE: Final[int] = 100


# ============================================================================
# Request Context Headers
# ============================================================================

REQUEST_ID_HEADER: Final[str] = "X-Request-ID"

CORRELATION_ID_HEADER: Final[str] = "X-Correlation-ID"

TENANT_ID_HEADER: Final[str] = "X-Tenant-ID"

ORGANIZATION_ID_HEADER: Final[str] = "X-Organization-ID"


# ============================================================================
# Health
# ============================================================================

HEALTHY: Final[str] = "healthy"

UNHEALTHY: Final[str] = "unhealthy"

DEGRADED: Final[str] = "degraded"

ALIVE: Final[str] = "alive"

READY: Final[str] = "ready"

NOT_READY: Final[str] = "not_ready"


# ============================================================================
# Service Status
# ============================================================================

SERVICE_UP: Final[str] = "up"

SERVICE_DOWN: Final[str] = "down"

SERVICE_DEGRADED: Final[str] = "degraded"


# ============================================================================
# Health Endpoints
# ============================================================================

HEALTH_ENDPOINT: Final[str] = "/health/"

LIVE_ENDPOINT: Final[str] = "/health/live/"

READY_ENDPOINT: Final[str] = "/health/ready/"


# ============================================================================
# Security
# ============================================================================

DEFAULT_TOKEN_EXPIRY_MINUTES: Final[int] = 30

PASSWORD_MIN_LENGTH: Final[int] = 8


__all__ = [
    "ALIVE",
    "APP_NAME",
    "APP_VERSION",
    "API_VERSION",
    "CORRELATION_ID_HEADER",
    "DEGRADED",
    "DEFAULT_API_VERSION",
    "DEFAULT_CHARSET",
    "DEFAULT_PAGE_SIZE",
    "DEFAULT_TIME_ZONE",
    "DEFAULT_TOKEN_EXPIRY_MINUTES",
    "HEALTH_ENDPOINT",
    "HEALTHY",
    "LIVE_ENDPOINT",
    "MAX_PAGE_SIZE",
    "MINIMUM_PYTHON_VERSION",
    "NOT_READY",
    "ORGANIZATION_ID_HEADER",
    "PASSWORD_MIN_LENGTH",
    "READY",
    "READY_ENDPOINT",
    "REQUEST_ID_HEADER",
    "SERVICE_DEGRADED",
    "SERVICE_DOWN",
    "SERVICE_UP",
    "TENANT_ID_HEADER",
    "UNHEALTHY",
]
