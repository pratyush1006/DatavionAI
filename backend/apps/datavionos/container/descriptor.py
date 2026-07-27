"""
DatavionOS Service Descriptor.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeAlias, TypeVar

from apps.datavionos.container.lifetime import (
    ServiceLifetime,
)

TService = TypeVar("TService")

FactoryType: TypeAlias = Callable[..., Any]


@dataclass(
    frozen=True,
    slots=True,
)
class ServiceDescriptor:
    """
    Immutable service registration.

    A descriptor contains all metadata
    required by the dependency injection
    framework to construct and manage a
    service instance.
    """

    service_type: type[Any]

    implementation_type: type[Any] | None = None

    factory: FactoryType | None = None

    instance: Any | None = None

    lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT

    name: str | None = None

    metadata: dict[str, Any] | None = None

    @property
    def has_factory(
        self,
    ) -> bool:
        """
        Whether the descriptor uses
        a factory.
        """

        return self.factory is not None

    @property
    def has_instance(
        self,
    ) -> bool:
        """
        Whether the descriptor has an
        existing instance.
        """

        return self.instance is not None

    @property
    def has_implementation(
        self,
    ) -> bool:
        """
        Whether an implementation type
        exists.
        """

        return self.implementation_type is not None

    @property
    def implementation(
        self,
    ) -> type[Any]:
        """
        Effective implementation type.
        """

        return self.implementation_type or self.service_type

    @property
    def registration_name(
        self,
    ) -> str:
        """
        Registration identifier.
        """

        return self.name or self.service_type.__qualname__

    @property
    def is_singleton(
        self,
    ) -> bool:
        return self.lifetime.is_singleton

    @property
    def is_scoped(
        self,
    ) -> bool:
        return self.lifetime.is_scoped

    @property
    def is_transient(
        self,
    ) -> bool:
        return self.lifetime.is_transient

    @property
    def is_instance_registration(
        self,
    ) -> bool:
        """
        Indicates an existing instance
        was registered.
        """

        return self.has_instance

    @property
    def is_factory_registration(
        self,
    ) -> bool:
        """
        Indicates a factory registration.
        """

        return self.has_factory

    @property
    def is_type_registration(
        self,
    ) -> bool:
        """
        Indicates a type registration.
        """

        return (
            self.has_implementation and not self.has_factory and not self.has_instance
        )

    @property
    def cacheable(
        self,
    ) -> bool:
        """
        Whether resolved instances may
        be cached.
        """

        return self.lifetime.is_cacheable

    def with_metadata(
        self,
        **metadata: Any,
    ) -> ServiceDescriptor:
        """
        Return a new descriptor with
        merged metadata.
        """

        updated = dict(
            self.metadata or {},
        )

        updated.update(
            metadata,
        )

        return ServiceDescriptor(
            service_type=self.service_type,
            implementation_type=self.implementation_type,
            factory=self.factory,
            instance=self.instance,
            lifetime=self.lifetime,
            name=self.name,
            metadata=updated,
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "ServiceDescriptor("
            f"service={self.service_type.__qualname__}, "
            f"implementation={self.implementation.__qualname__}, "
            f"lifetime={self.lifetime})"
        )


__all__ = [
    "FactoryType",
    "ServiceDescriptor",
]
