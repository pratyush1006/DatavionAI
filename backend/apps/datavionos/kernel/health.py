"""
DatavionOS Kernel Health.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Protocol


@unique
class HealthStatus(
    Enum,
):
    """
    Runtime health status.
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

    def __str__(
        self,
    ) -> str:
        return self.value


class HealthCheck(
    Protocol,
):
    """
    Contract for runtime health checks.
    """

    @property
    def name(
        self,
    ) -> str:
        """
        Health check name.
        """

    async def check(
        self,
    ) -> HealthResult:
        """
        Execute the health check.
        """


@dataclass(
    frozen=True,
    slots=True,
)
class HealthResult:
    """
    Result of a single health check.
    """

    name: str

    status: HealthStatus

    message: str = ""

    duration_ms: float = 0.0


@dataclass(
    slots=True,
)
class KernelHealth:
    """
    Aggregates runtime health checks.
    """

    checks: list[HealthCheck] = field(
        default_factory=list,
    )

    async def execute(
        self,
    ) -> list[HealthResult]:
        """
        Execute all registered health
        checks.
        """

        results: list[HealthResult] = []

        for check in self.checks:
            results.append(
                await check.check(),
            )

        return results

    async def status(
        self,
    ) -> HealthStatus:
        """
        Compute overall runtime health.
        """

        results = await self.execute()

        if any(result.status is HealthStatus.UNHEALTHY for result in results):
            return HealthStatus.UNHEALTHY

        if any(result.status is HealthStatus.DEGRADED for result in results):
            return HealthStatus.DEGRADED

        return HealthStatus.HEALTHY

    async def is_healthy(
        self,
    ) -> bool:
        """
        Whether the runtime is healthy.
        """

        return await self.status() is HealthStatus.HEALTHY

    def register(
        self,
        check: HealthCheck,
    ) -> None:
        """
        Register a health check.
        """

        self.checks.append(
            check,
        )

    def unregister(
        self,
        check: HealthCheck,
    ) -> None:
        """
        Remove a health check.
        """

        self.checks.remove(
            check,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all health checks.
        """

        self.checks.clear()

    @property
    def count(
        self,
    ) -> int:
        """
        Number of registered checks.
        """

        return len(
            self.checks,
        )

    def __repr__(
        self,
    ) -> str:
        return f"KernelHealth(checks={self.count})"


__all__ = [
    "HealthStatus",
    "HealthCheck",
    "HealthResult",
    "KernelHealth",
]
