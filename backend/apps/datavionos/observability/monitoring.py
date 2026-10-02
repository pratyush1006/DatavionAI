"""
Monitoring contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.observability.diagnostics import (
    DiagnosticReport,
    DiagnosticsProvider,
)
from apps.datavionos.observability.events import (
    ObservationEvent,
    ObservationEventPublisher,
)
from apps.datavionos.observability.logger import (
    Logger,
)
from apps.datavionos.observability.metrics import (
    Metric,
    MetricsCollector,
)
from apps.datavionos.observability.tracing import (
    Trace,
    Tracer,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringSnapshot:
    """
    Immutable observability snapshot.
    """

    diagnostics: DiagnosticReport

    metrics: tuple[Metric, ...]

    traces: tuple[Trace, ...]

    events: tuple[ObservationEvent, ...]


@runtime_checkable
class MonitoringService(
    Protocol,
):
    """
    Coordinates platform observability.
    """

    @property
    def logger(
        self,
    ) -> Logger:
        """
        Return the logger.
        """

    @property
    def metrics(
        self,
    ) -> MetricsCollector:
        """
        Return the metrics collector.
        """

    @property
    def tracer(
        self,
    ) -> Tracer:
        """
        Return the tracer.
        """

    @property
    def events(
        self,
    ) -> ObservationEventPublisher:
        """
        Return the event publisher.
        """

    @property
    def diagnostics(
        self,
    ) -> DiagnosticsProvider:
        """
        Return the diagnostics provider.
        """

    async def snapshot(
        self,
    ) -> MonitoringSnapshot:
        """
        Collect a unified observability snapshot.
        """

    async def flush(
        self,
    ) -> None:
        """
        Flush buffered telemetry.
        """


__all__ = [
    "MonitoringService",
    "MonitoringSnapshot",
]
