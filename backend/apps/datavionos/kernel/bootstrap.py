"""
DatavionOS Kernel Bootstrap.

The kernel bootstrap is responsible for assembling the
runtime service collection without depending on a specific
dependency-injection container implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apps.datavionos.kernel.configuration import (
    KernelConfiguration,
)
from apps.datavionos.kernel.environment import (
    KernelEnvironment,
)
from apps.datavionos.kernel.exceptions import (
    BootstrapError,
)


@dataclass(
    slots=True,
)
class KernelBootstrap:
    """
    Responsible for assembling the DatavionOS runtime.

    The kernel intentionally does not depend on a concrete
    dependency-injection container. Runtime services are
    collected explicitly and handed to KernelRuntime.

    Dependency resolution, when required by a concrete
    application service, belongs to the application/runtime
    composition layer rather than the kernel bootstrap.
    """

    configuration: KernelConfiguration

    environment: KernelEnvironment

    services: list[object] = field(
        default_factory=list,
    )

    async def bootstrap(
        self,
    ) -> list[object]:
        """
        Bootstrap the runtime and return the configured
        runtime services.

        The returned collection is intentionally a plain list
        so the kernel remains independent of any DI container.
        """

        try:
            await self._validate()

            await self._register_services()

            await self._initialize()

            return list(
                self.services,
            )

        except BootstrapError:
            raise

        except Exception as exc:
            raise BootstrapError(
                "Kernel bootstrap failed.",
            ) from exc

    async def _validate(
        self,
    ) -> None:
        """
        Validate runtime prerequisites.
        """

        if not self.configuration.application_name:
            raise BootstrapError(
                "Application name is required.",
            )

        if self.configuration.request_timeout <= 0:
            raise BootstrapError(
                "Invalid request timeout.",
            )

        if self.configuration.shutdown_timeout <= 0:
            raise BootstrapError(
                "Invalid shutdown timeout.",
            )

        if self.configuration.health_check_interval <= 0:
            raise BootstrapError(
                "Invalid health check interval.",
            )

        if self.configuration.max_parallel_tasks <= 0:
            raise BootstrapError(
                "Invalid maximum parallel task count.",
            )

    async def _register_services(
        self,
    ) -> None:
        """
        Register runtime services.

        Concrete service registration is intentionally delegated
        to the application composition layer.

        This method exists as the kernel extension point for
        future platform-level runtime services without coupling
        the kernel to a dependency-injection implementation.
        """

        return

    async def _initialize(
        self,
    ) -> None:
        """
        Perform bootstrap-level initialization.

        Individual runtime service lifecycle operations are
        coordinated by KernelRuntime and KernelLifecycle.
        """

        return

    def register_service(
        self,
        service: object,
    ) -> None:
        """
        Register a runtime-managed service.

        Services are kept as plain objects. Lifecycle support is
        detected by KernelLifecycle through the supported method
        contracts.
        """

        if service not in self.services:
            self.services.append(
                service,
            )

    def unregister_service(
        self,
        service: object,
    ) -> None:
        """
        Remove a runtime-managed service.

        Raises ValueError when the service is not registered.
        """

        self.services.remove(
            service,
        )

    @classmethod
    def create(
        cls,
        configuration: KernelConfiguration,
    ) -> KernelBootstrap:
        """
        Create a bootstrap instance using discovered defaults.
        """

        return cls(
            configuration=configuration,
            environment=KernelEnvironment.discover(),
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "KernelBootstrap("
            f"application={self.configuration.application_name}, "
            f"environment={self.environment.environment}, "
            f"services={len(self.services)})"
        )


__all__ = [
    "KernelBootstrap",
]
