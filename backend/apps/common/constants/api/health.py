"""
DatavionAI API Health Constants.

Centralized health monitoring constants used throughout the DatavionAI
platform.

This module defines health statuses, health check types, health component
names, probe endpoints, dependency categories, and response metadata for
application health monitoring.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Health Status
###############################################################################


class HealthStatus(StrEnum):
    """
    Standard health status values.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"

    UNKNOWN = "unknown"


SUPPORTED_HEALTH_STATUSES: Final[tuple[str, ...]] = (
    HealthStatus.HEALTHY.value,
    HealthStatus.DEGRADED.value,
    HealthStatus.UNHEALTHY.value,
    HealthStatus.UNKNOWN.value,
)

###############################################################################
# Health Check Types
###############################################################################


class HealthCheckType(StrEnum):
    """
    Supported health check categories.
    """

    LIVENESS = "liveness"

    READINESS = "readiness"

    STARTUP = "startup"

    DEPENDENCY = "dependency"


SUPPORTED_HEALTH_CHECKS: Final[tuple[str, ...]] = (
    HealthCheckType.LIVENESS.value,
    HealthCheckType.READINESS.value,
    HealthCheckType.STARTUP.value,
    HealthCheckType.DEPENDENCY.value,
)

###############################################################################
# Health Components
###############################################################################

COMPONENT_APPLICATION: Final[str] = "application"

COMPONENT_DATABASE: Final[str] = "database"

COMPONENT_CACHE: Final[str] = "cache"

COMPONENT_STORAGE: Final[str] = "storage"

COMPONENT_QUEUE: Final[str] = "queue"

COMPONENT_SEARCH: Final[str] = "search"

COMPONENT_EMAIL: Final[str] = "email"

COMPONENT_SMS: Final[str] = "sms"

COMPONENT_NOTIFICATION: Final[str] = "notification"

COMPONENT_REDIS: Final[str] = "redis"

COMPONENT_OBJECT_STORAGE: Final[str] = "object_storage"

COMPONENT_EXTERNAL_API: Final[str] = "external_api"

###############################################################################
# Kubernetes Probe Names
###############################################################################

PROBE_LIVENESS: Final[str] = "liveness"

PROBE_READINESS: Final[str] = "readiness"

PROBE_STARTUP: Final[str] = "startup"

###############################################################################
# Health Response Keys
###############################################################################

KEY_STATUS: Final[str] = "status"

KEY_COMPONENTS: Final[str] = "components"

KEY_CHECKS: Final[str] = "checks"

KEY_NAME: Final[str] = "name"

KEY_DURATION: Final[str] = "duration"

KEY_TIMESTAMP: Final[str] = "timestamp"

KEY_VERSION: Final[str] = "version"

KEY_DETAILS: Final[str] = "details"

###############################################################################
# Dependency Categories
###############################################################################

DEPENDENCY_REQUIRED: Final[str] = "required"

DEPENDENCY_OPTIONAL: Final[str] = "optional"

DEPENDENCY_EXTERNAL: Final[str] = "external"

###############################################################################
# Timeout Defaults (Seconds)
###############################################################################

DEFAULT_HEALTH_TIMEOUT: Final[int] = 5

DEFAULT_DEPENDENCY_TIMEOUT: Final[int] = 3

###############################################################################
# Reserved Components
###############################################################################

CORE_HEALTH_COMPONENTS: Final[frozenset[str]] = frozenset(
    {
        COMPONENT_APPLICATION,
        COMPONENT_DATABASE,
        COMPONENT_CACHE,
        COMPONENT_STORAGE,
    }
)

OPTIONAL_HEALTH_COMPONENTS: Final[frozenset[str]] = frozenset(
    {
        COMPONENT_QUEUE,
        COMPONENT_SEARCH,
        COMPONENT_EMAIL,
        COMPONENT_SMS,
        COMPONENT_NOTIFICATION,
        COMPONENT_REDIS,
        COMPONENT_OBJECT_STORAGE,
        COMPONENT_EXTERNAL_API,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "HealthStatus",
    "HealthCheckType",
)
