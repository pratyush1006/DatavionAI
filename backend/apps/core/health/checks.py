"""
Health check utilities for the Core application.
"""

from __future__ import annotations

import logging
from typing import TypedDict

from django.db import connection
from django.db.utils import DatabaseError

from apps.core.constants import (
    HEALTHY,
    UNHEALTHY,
)

logger = logging.getLogger(__name__)


class HealthCheckResult(TypedDict):
    """
    Represents the result of a health check.
    """

    status: str
    healthy: bool
    message: str


def database_health_check() -> HealthCheckResult:
    """
    Check whether the database is reachable.
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1;",
            )

        return {
            "status": HEALTHY,
            "healthy": True,
            "message": "Database connection is healthy.",
        }

    except DatabaseError:
        logger.exception(
            "Database health check failed.",
        )

        return {
            "status": UNHEALTHY,
            "healthy": False,
            "message": "Database connection failed.",
        }


def application_health_checks() -> dict[
    str,
    HealthCheckResult,
]:
    """
    Execute all registered application health checks.
    """

    return {
        "database": database_health_check(),
    }


def is_application_ready() -> bool:
    """
    Return whether the application is ready to serve requests.
    """

    return all(result["healthy"] for result in application_health_checks().values())


__all__ = [
    "HealthCheckResult",
    "application_health_checks",
    "database_health_check",
    "is_application_ready",
]
