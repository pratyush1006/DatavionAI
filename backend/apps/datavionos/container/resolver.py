"""
DatavionOS Service Resolver.
"""

from __future__ import annotations

import inspect
from typing import Any, TypeVar

from apps.datavionos.container.descriptor import (
    ServiceDescriptor,
)
from apps.datavionos.container.exceptions import (
    CircularDependencyError,
    ServiceNotFoundError,
)
from apps.datavionos.container.lifetime import (
    ServiceLifetime,
)
from apps.datavionos.container.registry import (
    ServiceRegistry,
)
from apps.datavionos.container.scope import (
    ServiceScope,
)

TService = TypeVar("TService")


class ServiceResolver:
    """
    Resolves services from the
    dependency injection container.
    """

    def __init__(
        self,
    ) -> None:
        self._singleton_instances: dict[
            type[Any],
            Any,
        ] = {}

    def resolve(
        self,
        *,
        service_type: type[TService],
        registry: ServiceRegistry,
        scope: ServiceScope,
    ) -> TService:
        """
        Resolve a service.
        """

        return self._resolve(
            service_type=service_type,
            registry=registry,
            scope=scope,
            dependency_chain=[],
        )

    def _resolve(
        self,
        *,
        service_type: type[Any],
        registry: ServiceRegistry,
        scope: ServiceScope,
        dependency_chain: list[str],
    ) -> Any:
        """
        Internal recursive resolver.
        """

        if service_type.__qualname__ in dependency_chain:
            raise CircularDependencyError(
                dependency_chain
                + [
                    service_type.__qualname__,
                ],
            )

        descriptor = registry.try_get(
            service_type,
        )

        if descriptor is None:
            raise ServiceNotFoundError(
                service_type.__qualname__,
            )

        dependency_chain = [
            *dependency_chain,
            service_type.__qualname__,
        ]

        if descriptor.has_instance:
            return descriptor.instance

        if descriptor.lifetime is ServiceLifetime.SINGLETON:
            cached = self._singleton_instances.get(
                service_type,
            )

            if cached is not None:
                return cached

            instance = self._create_instance(
                descriptor=descriptor,
                registry=registry,
                scope=scope,
                dependency_chain=dependency_chain,
            )

            self._singleton_instances[service_type] = instance

            return instance

        if descriptor.lifetime is ServiceLifetime.SCOPED:
            cached = scope.try_get(
                service_type,
            )

            if cached is not None:
                return cached

            instance = self._create_instance(
                descriptor=descriptor,
                registry=registry,
                scope=scope,
                dependency_chain=dependency_chain,
            )

            scope.set(
                service_type,
                instance,
            )

            return instance

        return self._create_instance(
            descriptor=descriptor,
            registry=registry,
            scope=scope,
            dependency_chain=dependency_chain,
        )

    def _create_instance(
        self,
        *,
        descriptor: ServiceDescriptor,
        registry: ServiceRegistry,
        scope: ServiceScope,
        dependency_chain: list[str],
    ) -> Any:
        """
        Construct a service instance.
        """

        if descriptor.has_factory:
            return descriptor.factory()

        implementation = descriptor.implementation

        constructor = implementation.__init__

        signature = inspect.signature(
            constructor,
        )

        dependencies: list[Any] = []

        parameters = list(
            signature.parameters.values(),
        )[1:]

        for parameter in parameters:
            if parameter.annotation is inspect._empty:
                raise TypeError(
                    (f"Missing type annotation for parameter {parameter.name}."),
                )

            dependency = self._resolve(
                service_type=parameter.annotation,
                registry=registry,
                scope=scope,
                dependency_chain=dependency_chain,
            )

            dependencies.append(
                dependency,
            )

        return implementation(
            *dependencies,
        )

    def clear_singletons(
        self,
    ) -> None:
        """
        Clear singleton cache.
        """

        self._singleton_instances.clear()

    @property
    def singleton_count(
        self,
    ) -> int:
        """
        Number of cached singletons.
        """

        return len(
            self._singleton_instances,
        )

    def __repr__(
        self,
    ) -> str:
        return f"ServiceResolver(singletons={self.singleton_count})"


__all__ = [
    "ServiceResolver",
]
