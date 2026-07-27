"""
Dependency injection container exceptions.
"""

from __future__ import annotations


class ContainerError(
    Exception,
):
    """
    Base container exception.
    """


class ServiceNotRegisteredError(
    ContainerError,
):
    """
    Raised when a requested service is not registered.
    """


class DuplicateServiceRegistrationError(
    ContainerError,
):
    """
    Raised when attempting to register a service that already exists.
    """


class InvalidServiceRegistrationError(
    ContainerError,
):
    """
    Raised when a service registration is invalid.
    """


class CircularDependencyError(
    ContainerError,
):
    """
    Raised when a circular dependency is detected.
    """


class ScopedServiceResolutionError(
    ContainerError,
):
    """
    Raised when a scoped service is resolved outside a valid scope.
    """


__all__ = [
    "CircularDependencyError",
    "ContainerError",
    "DuplicateServiceRegistrationError",
    "InvalidServiceRegistrationError",
    "ScopedServiceResolutionError",
    "ServiceNotRegisteredError",
]
