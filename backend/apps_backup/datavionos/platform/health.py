"""
Platform health contracts.
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
    Health check result status.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"


class HealthProbe(
    StrEnum,
):
    """
    Health probe category.
    """

    LIVENESS = "liveness"

    READINESS = "readiness"

    STARTUP = "startup"


@dataclass(
    frozen=True,
    slots=True,
)
class HealthResult:
    """
    Result returned by a health check.
    """

    status: HealthStatus

    description: str | None = None

    duration_ms: float | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class HealthCheck(
    Protocol,
):
    """
    Platform health check.
    """

    @property
    def name(
        self,
    ) -> str:
        """
        Health check name.
        """

    @property
    def probe(
        self,
    ) -> HealthProbe:
        """
        Probe type.
        """

    async def execute(
        self,
    ) -> HealthResult:
        """
        Execute the health check.
        """


@runtime_checkable
class HealthRegistry(
    Protocol,
):
    """
    Platform health registry.
    """

    def register(
        self,
        health_check: HealthCheck,
    ) -> None:
        """
        Register a health check.
        """

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a health check.
        """

    async def execute(
        self,
        probe: HealthProbe | None = None,
    ) -> dict[str, HealthResult]:
        """
        Execute registered health
        checks.
        """

    async def overall_status(
        self,
        probe: HealthProbe | None = None,
    ) -> HealthStatus:
        """
        Calculate overall platform
        health.
        """


__all__ = [
    "HealthStatus",
    "HealthProbe",
    "HealthResult",
    "HealthCheck",
    "HealthRegistry",
]
