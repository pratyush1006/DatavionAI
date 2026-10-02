"""
DatavionOS observability contracts.
"""

from __future__ import annotations

from .diagnostics import (
    Diagnostic,
    DiagnosticReport,
    DiagnosticsProvider,
    DiagnosticStatus,
)
from .events import (
    ObservationEvent,
    ObservationEventPublisher,
    ObservationEventType,
)
from .exceptions import (
    DiagnosticsError,
    LoggingError,
    MetricsError,
    MonitoringError,
    ObservabilityError,
    ObservationEventError,
    TracingError,
)
from .logger import (
    Logger,
    LogLevel,
    LogRecord,
)
from .metrics import (
    Metric,
    MetricsCollector,
    MetricType,
)
from .monitoring import (
    MonitoringService,
    MonitoringSnapshot,
)
from .services import (
    ObservabilityServices,
)
from .tracing import (
    Span,
    Trace,
    Tracer,
)

__all__ = [
    # Logging
    "Logger",
    "LogLevel",
    "LogRecord",
    # Metrics
    "Metric",
    "MetricType",
    "MetricsCollector",
    # Tracing
    "Span",
    "Trace",
    "Tracer",
    # Events
    "ObservationEvent",
    "ObservationEventType",
    "ObservationEventPublisher",
    # Diagnostics
    "Diagnostic",
    "DiagnosticReport",
    "DiagnosticStatus",
    "DiagnosticsProvider",
    # Monitoring
    "MonitoringSnapshot",
    "MonitoringService",
    # Service aggregation
    "ObservabilityServices",
    # Exceptions
    "ObservabilityError",
    "LoggingError",
    "MetricsError",
    "TracingError",
    "ObservationEventError",
    "DiagnosticsError",
    "MonitoringError",
]
