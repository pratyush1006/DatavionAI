"""
DatavionOS Container Builder.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from apps.datavionos.container.descriptor import (
    FactoryType,
    ServiceDescriptor,
)
from apps.datavionos.container.exceptions import (
    DuplicateRegistrationError,
)
from apps.datavionos.container.lifetime import (
    ServiceLifetime,
)
from apps.datavionos.container.provider import (
    ServiceProvider,
)
from apps.datavionos.container.registry import (
    ServiceRegistry,
)
from apps.datavionos.container.resolver import (
    ServiceResolver,
)

TService = TypeVar("TService")


class ContainerBuilder:
    """
    Builds the DatavionOS dependency
    injection container.
    """

    def __init__(
        self,
    ) -> None:
        self._registry = ServiceRegistry()
        self._frozen = False

    @property
    def registry(
        self,
    ) -> ServiceRegistry:
        return self._registry

    @property
    def is_frozen(
        self,
    ) -> bool:
        return self._frozen

    def add_singleton(
        self,
        service_type: type[TService],
        implementation: type[TService] | None = None,
        *,
        factory: FactoryType | None = None,
        instance: TService | None = None,
    ) -> ContainerBuilder:
        """
        Register a singleton service.
        """

        return self._register(
            service_type=service_type,
            implementation=implementation,
            factory=factory,
            instance=instance,
            lifetime=ServiceLifetime.SINGLETON,
        )

    def add_scoped(
        self,
        service_type: type[TService],
        implementation: type[TService] | None = None,
        *,
        factory: FactoryType | None = None,
    ) -> ContainerBuilder:
        """
        Register a scoped service.
        """

        return self._register(
            service_type=service_type,
            implementation=implementation,
            factory=factory,
            lifetime=ServiceLifetime.SCOPED,
        )

    def add_transient(
        self,
        service_type: type[TService],
        implementation: type[TService] | None = None,
        *,
        factory: FactoryType | None = None,
    ) -> ContainerBuilder:
        """
        Register a transient service.
        """

        return self._register(
            service_type=service_type,
            implementation=implementation,
            factory=factory,
            lifetime=ServiceLifetime.TRANSIENT,
        )

    def add_instance(
        self,
        service_type: type[TService],
        instance: TService,
    ) -> ContainerBuilder:
        """
        Register an existing instance.
        """

        return self.add_singleton(
            service_type=service_type,
            instance=instance,
        )

    def build(
        self,
    ) -> ServiceProvider:
        """
        Build the service provider.
        """

        self._frozen = True

        resolver = ServiceResolver()

        return ServiceProvider(
            registry=self._registry,
            resolver=resolver,
        )

    def _register(
        self,
        *,
        service_type: type[Any],
        implementation: type[Any] | None = None,
        factory: Callable[..., Any] | None = None,
        instance: Any | None = None,
        lifetime: ServiceLifetime,
    ) -> ContainerBuilder:
        """
        Internal registration helper.
        """

        if self._frozen:
            raise RuntimeError(
                "Container has already been built.",
            )

        if self._registry.contains(
            service_type,
        ):
            raise DuplicateRegistrationError(
                service_type.__qualname__,
            )

        descriptor = ServiceDescriptor(
            service_type=service_type,
            implementation_type=implementation,
            factory=factory,
            instance=instance,
            lifetime=lifetime,
        )

        self._registry.register(
            descriptor,
        )

        return self

    def __repr__(
        self,
    ) -> str:
        return (
            "ContainerBuilder("
            f"registrations={self._registry.count}, "
            f"frozen={self._frozen})"
        )


__all__ = [
    "ContainerBuilder",
]
