"""
DatavionOS Module Context.

Provides the runtime context shared with DatavionOS modules
without coupling modules to a concrete dependency-injection
container implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

from apps.datavionos.kernel import (
    KernelConfiguration,
    KernelEnvironment,
)
from apps.datavionos.queries import (
    QueryBus,
)


TService = TypeVar(
    "TService",
)


class ServiceResolver(Protocol):
    """
    Runtime service-resolution contract.

    The module layer depends only on this protocol and therefore
    remains independent of any concrete dependency-injection
    implementation.
    """

    def resolve(
        self,
        service_type: type[TService],
    ) -> TService:
        """
        Resolve a registered service.
        """
        ...


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleContext:
    """
    Runtime context shared with every
    DatavionOS module.

    Provides controlled access to platform infrastructure
    without exposing kernel or dependency-injection internals.
    """

    service_provider: ServiceResolver

    command_bus: CommandBus

    query_bus: QueryBus

    event_bus: EventBus

    configuration: KernelConfiguration

    environment: KernelEnvironment

    @property
    def is_development(
        self,
    ) -> bool:
        """
        Whether the runtime is executing
        in development mode.
        """

        return self.environment.is_development

    @property
    def is_testing(
        self,
    ) -> bool:
        """
        Whether the runtime is executing
        in testing mode.
        """

        return self.environment.is_testing

    @property
    def is_production(
        self,
    ) -> bool:
        """
        Whether the runtime is executing
        in production mode.
        """

        return self.environment.is_production

    def get_service(
        self,
        service_type: type[TService],
    ) -> TService:
        """
        Resolve a runtime service.

        Service resolution is provided by the DatavionOS runtime
        infrastructure through the ServiceResolver contract.
        The module context is intentionally not coupled to a
        concrete dependency-injection container.
        """

        return self.service_provider.resolve(
            service_type,
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "ModuleContext("
            f"environment={self.environment.environment}, "
            f"application={self.configuration.application_name})"
        )


__all__ = [
    "ModuleContext",
    "ServiceResolver",
]
