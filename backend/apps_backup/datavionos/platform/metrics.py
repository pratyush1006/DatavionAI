"""
Platform metrics contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

MetricTags = dict[str, str]


@runtime_checkable
class MetricsCollector(
    Protocol,
):
    """
    Platform metrics abstraction.

    Supports enterprise observability
    platforms such as:

    - Prometheus
    - OpenTelemetry
    - Azure Monitor
    - Datadog
    - CloudWatch
    """

    def increment(
        self,
        name: str,
        value: int = 1,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Increment a counter metric.
        """

    def decrement(
        self,
        name: str,
        value: int = 1,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Decrement a counter metric.
        """

    def gauge(
        self,
        name: str,
        value: int | float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Record a gauge metric.
        """

    def histogram(
        self,
        name: str,
        value: int | float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Record a histogram value.
        """

    def timing(
        self,
        name: str,
        duration_ms: float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Record execution time.
        """

    def record(
        self,
        name: str,
        value: int | float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        """
        Record a generic metric.
        """


@runtime_checkable
class Timer(
    Protocol,
):
    """
    Disposable timer used to
    automatically measure execution
    duration.
    """

    def __enter__(
        self,
    ) -> Timer: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None: ...


__all__ = [
    "MetricTags",
    "MetricsCollector",
    "Timer",
]
