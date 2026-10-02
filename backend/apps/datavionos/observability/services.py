"""
Observability service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.observability.diagnostics import (
    DiagnosticsProvider,
)
from apps.datavionos.observability.events import (
    ObservationEventPublisher,
)
from apps.datavionos.observability.logger import (
    Logger,
)
from apps.datavionos.observability.metrics import (
    MetricsCollector,
)
from apps.datavionos.observability.monitoring import (
    MonitoringService,
)
from apps.datavionos.observability.tracing import (
    Tracer,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ObservabilityServices:
    """
    Aggregate of observability services.
    """

    monitoring: MonitoringService

    logger: Logger

    metrics: MetricsCollector

    tracer: Tracer

    events: ObservationEventPublisher

    diagnostics: DiagnosticsProvider


__all__ = [
    "ObservabilityServices",
]
