"""
Platform service exceptions.
"""

from __future__ import annotations


class PlatformError(Exception):
    """
    Base exception for all platform
    services.
    """


class LoggerError(PlatformError):
    """
    Raised when a logging operation
    fails.
    """


class MetricsError(PlatformError):
    """
    Raised when metrics collection
    fails.
    """


class TelemetryError(PlatformError):
    """
    Raised when telemetry or tracing
    operations fail.
    """


class AuditError(PlatformError):
    """
    Raised when audit operations
    fail.
    """


class FeatureFlagError(PlatformError):
    """
    Raised when feature flag
    evaluation fails.
    """


class ConfigurationProviderError(PlatformError):
    """
    Raised when configuration cannot
    be resolved.
    """


class HealthRegistryError(PlatformError):
    """
    Raised when registering or
    executing health checks fails.
    """


class SchedulerError(PlatformError):
    """
    Raised when scheduler operations
    fail.
    """


class CacheError(PlatformError):
    """
    Raised when cache operations
    fail.
    """


class StorageError(PlatformError):
    """
    Raised when storage operations
    fail.
    """


class NotificationError(PlatformError):
    """
    Raised when sending notifications
    fails.
    """


class SecretProviderError(PlatformError):
    """
    Raised when secrets cannot be
    retrieved.
    """


__all__ = [
    "PlatformError",
    "LoggerError",
    "MetricsError",
    "TelemetryError",
    "AuditError",
    "FeatureFlagError",
    "ConfigurationProviderError",
    "HealthRegistryError",
    "SchedulerError",
    "CacheError",
    "StorageError",
    "NotificationError",
    "SecretProviderError",
]
