"""
Observability exceptions.
"""

from __future__ import annotations


class ObservabilityError(Exception):
    """
    Base exception for the observability subsystem.
    """


class LoggingError(ObservabilityError):
    """
    Raised when a logging operation fails.
    """


class MetricsError(ObservabilityError):
    """
    Raised when a metrics operation fails.
    """


class TracingError(ObservabilityError):
    """
    Raised when a tracing operation fails.
    """


class ObservationEventError(ObservabilityError):
    """
    Raised when an observability event operation fails.
    """


class DiagnosticsError(ObservabilityError):
    """
    Raised when diagnostics collection fails.
    """


class MonitoringError(ObservabilityError):
    """
    Raised when monitoring operations fail.
    """


__all__ = [
    "ObservabilityError",
    "LoggingError",
    "MetricsError",
    "TracingError",
    "ObservationEventError",
    "DiagnosticsError",
    "MonitoringError",
]
