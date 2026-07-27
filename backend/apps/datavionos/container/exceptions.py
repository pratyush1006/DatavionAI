"""
DatavionOS Dependency Injection Exceptions.
"""

from __future__ import annotations


class ContainerError(Exception):
    """
    Base exception for the dependency
    injection framework.
    """


class RegistrationError(
    ContainerError,
):
    """
    Base exception raised during
    service registration.
    """


class DuplicateRegistrationError(
    RegistrationError,
):
    """
    Raised when attempting to register
    an already registered service.
    """

    def __init__(
        self,
        service_name: str,
    ) -> None:
        super().__init__(
            (f"Service '{service_name}' is already registered."),
        )

        self.service_name = service_name


class InvalidDescriptorError(
    RegistrationError,
):
    """
    Raised when a service descriptor
    is invalid.
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(
            message,
        )


class ResolutionError(
    ContainerError,
):
    """
    Base exception raised while
    resolving services.
    """


class ServiceNotFoundError(
    ResolutionError,
):
    """
    Raised when a service cannot
    be resolved.
    """

    def __init__(
        self,
        service_name: str,
    ) -> None:
        super().__init__(
            (f"Service '{service_name}' is not registered."),
        )

        self.service_name = service_name


class CircularDependencyError(
    ResolutionError,
):
    """
    Raised when a circular dependency
    is detected.
    """

    def __init__(
        self,
        dependency_chain: list[str],
    ) -> None:
        chain = " -> ".join(
            dependency_chain,
        )

        super().__init__(
            (f"Circular dependency detected: {chain}"),
        )

        self.dependency_chain = tuple(
            dependency_chain,
        )


class ScopeError(
    ContainerError,
):
    """
    Raised for invalid scope
    operations.
    """


class ContainerBuildError(
    ContainerError,
):
    """
    Raised when the container
    cannot be built.
    """


class FrozenContainerError(
    ContainerError,
):
    """
    Raised when attempting to modify
    a frozen container.
    """


__all__ = [
    "ContainerError",
    "RegistrationError",
    "DuplicateRegistrationError",
    "InvalidDescriptorError",
    "ResolutionError",
    "ServiceNotFoundError",
    "CircularDependencyError",
    "ScopeError",
    "ContainerBuildError",
    "FrozenContainerError",
]
