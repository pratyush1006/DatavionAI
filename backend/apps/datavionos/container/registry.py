"""
DatavionOS Service Registry.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from apps.datavionos.container.descriptor import (
    ServiceDescriptor,
)


class ServiceRegistry:
    """
    Stores service registrations for the
    dependency injection container.
    """

    def __init__(
        self,
    ) -> None:
        self._registrations: dict[
            type[Any],
            ServiceDescriptor,
        ] = {}

    @property
    def count(
        self,
    ) -> int:
        """
        Number of registered services.
        """

        return len(
            self._registrations,
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        """
        Whether the registry contains
        any registrations.
        """

        return not self._registrations

    def register(
        self,
        descriptor: ServiceDescriptor,
    ) -> None:
        """
        Register a service descriptor.
        """

        service_type = descriptor.service_type

        if service_type in self._registrations:
            raise ValueError(
                (f"{service_type.__qualname__} is already registered."),
            )

        self._registrations[service_type] = descriptor

    def replace(
        self,
        descriptor: ServiceDescriptor,
    ) -> None:
        """
        Replace or insert a descriptor.
        """

        self._registrations[descriptor.service_type] = descriptor

    def unregister(
        self,
        service_type: type[Any],
    ) -> None:
        """
        Remove a registration.
        """

        self._registrations.pop(
            service_type,
            None,
        )

    def contains(
        self,
        service_type: type[Any],
    ) -> bool:
        """
        Determine whether a service
        is registered.
        """

        return service_type in self._registrations

    def get(
        self,
        service_type: type[Any],
    ) -> ServiceDescriptor:
        """
        Retrieve a descriptor.
        """

        return self._registrations[service_type]

    def try_get(
        self,
        service_type: type[Any],
    ) -> ServiceDescriptor | None:
        """
        Retrieve a descriptor if present.
        """

        return self._registrations.get(
            service_type,
        )

    def registrations(
        self,
    ) -> tuple[
        ServiceDescriptor,
        ...,
    ]:
        """
        Return every registration.
        """

        return tuple(
            self._registrations.values(),
        )

    def service_types(
        self,
    ) -> tuple[
        type[Any],
        ...,
    ]:
        """
        Return registered service types.
        """

        return tuple(
            self._registrations.keys(),
        )

    def clear(
        self,
    ) -> None:
        """
        Remove every registration.
        """

        self._registrations.clear()

    def __contains__(
        self,
        service_type: type[Any],
    ) -> bool:
        return self.contains(
            service_type,
        )

    def __getitem__(
        self,
        service_type: type[Any],
    ) -> ServiceDescriptor:
        return self.get(
            service_type,
        )

    def __iter__(
        self,
    ) -> Iterator[ServiceDescriptor,]:
        return iter(
            self._registrations.values(),
        )

    def __len__(
        self,
    ) -> int:
        return self.count

    def __repr__(
        self,
    ) -> str:
        return f"ServiceRegistry(count={self.count})"


__all__ = [
    "ServiceRegistry",
]
