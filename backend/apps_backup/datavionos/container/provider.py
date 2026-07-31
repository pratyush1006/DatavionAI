"""
DatavionOS Service Provider.
"""

from __future__ import annotations

from typing import Any, TypeVar

from apps.datavionos.container.registry import (
    ServiceRegistry,
)
from apps.datavionos.container.resolver import (
    ServiceResolver,
)
from apps.datavionos.container.scope import (
    ServiceScope,
)

TService = TypeVar("TService")


class ServiceProvider:
    """
    Runtime service provider.

    Coordinates service resolution using
    the registry, resolver and execution
    scope.
    """

    def __init__(
        self,
        registry: ServiceRegistry,
        resolver: ServiceResolver,
        *,
        scope: ServiceScope | None = None,
    ) -> None:
        self._registry = registry
        self._resolver = resolver
        self._scope = scope or ServiceScope()

    @property
    def registry(
        self,
    ) -> ServiceRegistry:
        """
        Registered services.
        """

        return self._registry

    @property
    def resolver(
        self,
    ) -> ServiceResolver:
        """
        Service resolver.
        """

        return self._resolver

    @property
    def scope(
        self,
    ) -> ServiceScope:
        """
        Current execution scope.
        """

        return self._scope

    def get_service(
        self,
        service_type: type[TService],
    ) -> TService:
        """
        Resolve a required service.
        """

        return self._resolver.resolve(
            service_type=service_type,
            registry=self._registry,
            scope=self._scope,
        )

    def try_get_service(
        self,
        service_type: type[TService],
    ) -> TService | None:
        """
        Resolve an optional service.
        """

        try:
            return self.get_service(
                service_type,
            )

        except Exception:
            return None

    def create_scope(
        self,
    ) -> ServiceProvider:
        """
        Create a child provider with a
        new execution scope.
        """

        return ServiceProvider(
            registry=self._registry,
            resolver=self._resolver,
            scope=ServiceScope(
                parent=self._scope,
            ),
        )

    def dispose(
        self,
    ) -> None:
        """
        Dispose the current scope.
        """

        self._scope.dispose()

    def __contains__(
        self,
        service_type: type[Any],
    ) -> bool:
        return self._registry.contains(
            service_type,
        )

    def __getitem__(
        self,
        service_type: type[TService],
    ) -> TService:
        return self.get_service(
            service_type,
        )

    def __repr__(
        self,
    ) -> str:
        return f"ServiceProvider(scope={self._scope})"


__all__ = [
    "ServiceProvider",
]
