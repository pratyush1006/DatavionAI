"""
DatavionOS Kernel Bootstrap.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.container import (
    ContainerBuilder,
    ServiceProvider,
)
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
    Responsible for assembling the
    DatavionOS runtime.
    """

    configuration: KernelConfiguration

    environment: KernelEnvironment

    builder: ContainerBuilder

    async def bootstrap(
        self,
    ) -> ServiceProvider:
        """
        Bootstrap the runtime and
        return the configured
        service provider.
        """

        try:
            await self._validate()

            await self._register_services()

            provider = self.builder.build()

            await self._initialize(provider)

            return provider

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

    async def _register_services(
        self,
    ) -> None:
        """
        Register infrastructure
        services.

        Module registration will be
        delegated to the Module Loader.
        """

        return

    async def _initialize(
        self,
        provider: ServiceProvider,
    ) -> None:
        """
        Perform post-build
        initialization.

        Runtime initialization will
        later be coordinated by
        KernelRuntime.
        """

        _ = provider

        return

    @classmethod
    def create(
        cls,
        configuration: KernelConfiguration,
    ) -> KernelBootstrap:
        """
        Create a bootstrap instance
        using discovered defaults.
        """

        return cls(
            configuration=configuration,
            environment=KernelEnvironment.discover(),
            builder=ContainerBuilder(),
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "KernelBootstrap("
            f"application={self.configuration.application_name}, "
            f"environment={self.environment.environment})"
        )


__all__ = [
    "KernelBootstrap",
]
