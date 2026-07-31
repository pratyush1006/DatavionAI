"""
Metrics contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class MetricType(
    StrEnum,
):
    """
    Supported metric types.
    """

    COUNTER = "counter"

    GAUGE = "gauge"

    HISTOGRAM = "histogram"

    TIMER = "timer"


@dataclass(
    frozen=True,
    slots=True,
)
class Metric:
    """
    Immutable metric.
    """

    name: str

    type: MetricType

    value: float

    unit: str | None = None

    tags: dict[str, str] | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class MetricsCollector(
    Protocol,
):
    """
    Collects application metrics.
    """

    async def record(
        self,
        metric: Metric,
    ) -> None:
        """
        Record a metric.
        """

    async def increment(
        self,
        name: str,
        value: float = 1.0,
        **tags: str,
    ) -> None:
        """
        Increment a counter metric.
        """

    async def gauge(
        self,
        name: str,
        value: float,
        **tags: str,
    ) -> None:
        """
        Record a gauge metric.
        """

    async def histogram(
        self,
        name: str,
        value: float,
        **tags: str,
    ) -> None:
        """
        Record a histogram metric.
        """

    async def timer(
        self,
        name: str,
        duration: float,
        **tags: str,
    ) -> None:
        """
        Record a timing metric.
        """


__all__ = [
    "Metric",
    "MetricsCollector",
    "MetricType",
]
