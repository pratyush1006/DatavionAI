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

    Returns:
        The database health check result.
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")

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


def application_health_checks() -> dict[str, HealthCheckResult]:
    """
    Execute all registered application health checks.

    Returns:
        Dictionary containing the result of each health check.
    """

    return {
        "database": database_health_check(),
    }


def is_application_ready() -> bool:
    """
    Determine whether the application is ready to serve requests.

    Returns:
        True if every health check succeeds, otherwise False.
    """

    return all(result["healthy"] for result in application_health_checks().values())
