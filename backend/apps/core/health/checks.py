"""
Health check utilities for the Core application.
"""

from __future__ import annotations

import logging
import time
from datetime import UTC, datetime
from typing import NotRequired, TypedDict

from django.db import connection

from apps.core.constants import (
    HEALTHY,
    UNHEALTHY,
)

logger = logging.getLogger(__name__)


class HealthCheckResult(TypedDict):
    """
    Result of a health check.
    """

    component: str
    status: str
    healthy: bool
    message: str
    timestamp: str
    duration_ms: NotRequired[int]


class ApplicationHealthResult(TypedDict):
    """
    Overall application health.
    """

    status: str
    healthy: bool
    checks: dict[str, HealthCheckResult]


def _timestamp() -> str:
    """
    Return current UTC timestamp.
    """

    return (
        datetime.now(
            UTC,
        )
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    )


def database_health_check() -> HealthCheckResult:
    """
    Check database connectivity.
    """

    started = time.perf_counter()

    try:
        connection.ensure_connection()

        duration = round(
            (time.perf_counter() - started) * 1000,
        )

        return {
            "component": "database",
            "status": HEALTHY,
            "healthy": True,
            "message": "Database connection is healthy.",
            "timestamp": _timestamp(),
            "duration_ms": duration,
        }

    except Exception:
        logger.exception(
            "Database health check failed.",
        )

        duration = round(
            (time.perf_counter() - started) * 1000,
        )

        return {
            "component": "database",
            "status": UNHEALTHY,
            "healthy": False,
            "message": "Database connection failed.",
            "timestamp": _timestamp(),
            "duration_ms": duration,
        }


def application_health_checks() -> ApplicationHealthResult:
    """
    Execute all registered health checks.
    """

    checks = {
        "database": database_health_check(),
    }

    healthy = all(result["healthy"] for result in checks.values())

    return {
        "status": HEALTHY if healthy else UNHEALTHY,
        "healthy": healthy,
        "checks": checks,
    }


def is_application_ready() -> bool:
    """
    Return whether the application is ready
    to receive requests.
    """

    return application_health_checks()["healthy"]


__all__ = [
    "ApplicationHealthResult",
    "HealthCheckResult",
    "application_health_checks",
    "database_health_check",
    "is_application_ready",
]
