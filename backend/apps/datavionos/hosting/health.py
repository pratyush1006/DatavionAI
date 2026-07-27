"""
Application health contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class HealthStatus(
    StrEnum,
):
    """
    Health status.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"


@dataclass(
    frozen=True,
    slots=True,
)
class HealthReport:
    """
    Immutable application health report.
    """

    status: HealthStatus

    message: str | None = None

    details: dict[str, Any] | None = None


@runtime_checkable
class HealthChecker(
    Protocol,
):
    """
    Evaluates application health.
    """

    async def readiness(
        self,
    ) -> HealthReport:
        """
        Evaluate application readiness.
        """

    async def liveness(
        self,
    ) -> HealthReport:
        """
        Evaluate application liveness.
        """

    async def health(
        self,
    ) -> HealthReport:
        """
        Evaluate overall application health.
        """


__all__ = [
    "HealthChecker",
    "HealthReport",
    "HealthStatus",
]
