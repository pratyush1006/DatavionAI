"""
DatavionOS Dependency Injection Container.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


class Container(
    ABC,
):
    """
    Base dependency injection container.

    The container is responsible for
    resolving application services,
    infrastructure components and
    runtime dependencies.
    """

    @property
    def container_name(
        self,
    ) -> str:
        """
        Container implementation name.
        """

        return self.__class__.__qualname__

    @property
    def supports_scopes(
        self,
    ) -> bool:
        """
        Indicates whether scoped
        lifetimes are supported.
        """

        return True

    @property
    def supports_validation(
        self,
    ) -> bool:
        """
        Indicates whether dependency
        graph validation is supported.
        """

        return True

    @abstractmethod
    def register(
        self,
        service_type: type[T],
        implementation: type[T] | None = None,
        *,
        factory: Callable[..., T] | None = None,
        instance: T | None = None,
    ) -> None:
        """
        Register a service.
        """

    @abstractmethod
    def resolve(
        self,
        service_type: type[T],
    ) -> T:
        """
        Resolve a service.
        """

    @abstractmethod
    def try_resolve(
        self,
        service_type: type[T],
    ) -> T | None:
        """
        Attempt to resolve a service.
        """

    @abstractmethod
    def contains(
        self,
        service_type: type[Any],
    ) -> bool:
        """
        Determine whether a service
        is registered.
        """

    @abstractmethod
    def unregister(
        self,
        service_type: type[Any],
    ) -> None:
        """
        Remove a registration.
        """

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove every registration.
        """

    @abstractmethod
    def create_scope(
        self,
    ) -> Container:
        """
        Create a child scope.
        """

    @abstractmethod
    def validate(
        self,
    ) -> None:
        """
        Validate dependency graph.
        """

    @abstractmethod
    def registrations(
        self,
    ) -> tuple[type[Any], ...]:
        """
        Return registered services.
        """

    @abstractmethod
    def dispose(
        self,
    ) -> None:
        """
        Dispose container resources.
        """

    def __contains__(
        self,
        service_type: type[Any],
    ) -> bool:
        return self.contains(
            service_type,
        )

    def __getitem__(
        self,
        service_type: type[T],
    ) -> T:
        return self.resolve(
            service_type,
        )

    def __iter__(
        self,
    ) -> Iterator[type[Any]]:
        return iter(
            self.registrations(),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.container_name}("
            f"scopes={self.supports_scopes}, "
            f"validation={self.supports_validation})"
        )


__all__ = [
    "Container",
]
