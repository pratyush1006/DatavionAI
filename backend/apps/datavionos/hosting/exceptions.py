"""
Hosting exceptions.
"""

from __future__ import annotations


class HostingError(Exception):
    """
    Base hosting exception.
    """


class ApplicationError(HostingError):
    """
    Raised when an application operation fails.
    """


class EnvironmentError(HostingError):
    """
    Raised when an environment operation fails.
    """


class LifecycleError(HostingError):
    """
    Raised when an application lifecycle operation fails.
    """


class RuntimeProviderError(HostingError):
    """
    Raised when runtime information cannot be obtained.
    """


class HealthCheckError(HostingError):
    """
    Raised when a health check fails.
    """


class HostError(HostingError):
    """
    Raised when a host operation fails.
    """


__all__ = [
    "HostingError",
    "ApplicationError",
    "EnvironmentError",
    "LifecycleError",
    "RuntimeProviderError",
    "HealthCheckError",
    "HostError",
]
