"""
Dependency injection container.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from apps.infrastructure.container.exceptions import (
    ServiceNotRegisteredError,
)
from apps.infrastructure.container.registry import (
    ServiceLifetime,
    ServiceRegistration,
)
from apps.infrastructure.container.service_provider import (
    ServiceProvider,
)


class Container(
    ServiceProvider,
):
    """
    Default dependency injection container.
    """

    def __init__(
        self,
    ) -> None:
        self._registrations: dict[
            tuple[type[Any], str | None],
            ServiceRegistration,
        ] = {}

        self._singletons: dict[
            tuple[type[Any], str | None],
            Any,
        ] = {}

    def register(
        self,
        service_type: type[Any],
        implementation_type: type[Any],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        name: str | None = None,
    ) -> None:
        self._registrations[(service_type, name)] = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation_type,
            lifetime=lifetime,
            name=name,
        )

    def register_factory(
        self,
        service_type: type[Any],
        factory: Callable[..., Any],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        name: str | None = None,
    ) -> None:
        self._registrations[(service_type, name)] = ServiceRegistration(
            service_type=service_type,
            factory=factory,
            lifetime=lifetime,
            name=name,
        )

    def register_instance(
        self,
        service_type: type[Any],
        instance: Any,
        *,
        name: str | None = None,
    ) -> None:
        key = (service_type, name)

        self._registrations[key] = ServiceRegistration(
            service_type=service_type,
            instance=instance,
            lifetime=ServiceLifetime.SINGLETON,
            name=name,
        )

        self._singletons[key] = instance

    def resolve(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> Any:
        key = (service_type, name)

        registration = self._registrations.get(key)

        if registration is None:
            raise ServiceNotRegisteredError(f"{service_type!r} is not registered.")

        if registration.lifetime is ServiceLifetime.SINGLETON:
            if key in self._singletons:
                return self._singletons[key]

        instance = self._create_instance(
            registration,
        )

        if registration.lifetime is ServiceLifetime.SINGLETON:
            self._singletons[key] = instance

        return instance

    def is_registered(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> bool:
        return (
            service_type,
            name,
        ) in self._registrations

    def _create_instance(
        self,
        registration: ServiceRegistration,
    ) -> Any:
        if registration.instance is not None:
            return registration.instance

        if registration.factory is not None:
            return registration.factory()

        if registration.implementation_type is not None:
            return registration.implementation_type()

        raise RuntimeError("Invalid service registration.")


__all__ = [
    "Container",
]
