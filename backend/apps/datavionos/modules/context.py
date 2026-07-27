"""
DatavionOS Module Context.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.commands import (
    CommandBus,
)
from apps.datavionos.container import (
    ServiceProvider,
)
from apps.datavionos.events import (
    EventBus,
)
from apps.datavionos.kernel import (
    KernelConfiguration,
    KernelEnvironment,
)
from apps.datavionos.queries import (
    QueryBus,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleContext:
    """
    Runtime context shared with every
    DatavionOS module.

    Provides controlled access to the
    platform infrastructure without
    exposing kernel internals.
    """

    service_provider: ServiceProvider

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
        service_type: type,
    ) -> object:
        """
        Resolve a service from the
        dependency injection container.
        """

        return self.service_provider.get_service(
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
]
