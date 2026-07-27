"""
Service provider contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.infrastructure.container.registry import (
    ServiceLifetime,
)


@runtime_checkable
class ServiceProvider(
    Protocol,
):
    """
    Dependency injection service provider.
    """

    def register(
        self,
        service_type: type[Any],
        implementation_type: type[Any],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        name: str | None = None,
    ) -> None:
        """
        Register a service implementation.
        """

    def register_factory(
        self,
        service_type: type[Any],
        factory: Any,
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        name: str | None = None,
    ) -> None:
        """
        Register a service factory.
        """

    def register_instance(
        self,
        service_type: type[Any],
        instance: Any,
        *,
        name: str | None = None,
    ) -> None:
        """
        Register an existing singleton instance.
        """

    def resolve(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> Any:
        """
        Resolve a registered service.
        """

    def is_registered(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> bool:
        """
        Determine whether a service is registered.
        """


__all__ = [
    "ServiceProvider",
]
