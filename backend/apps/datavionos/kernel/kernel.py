"""
DatavionOS Kernel.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apps.datavionos.kernel.application import (
    KernelApplication,
)
from apps.datavionos.kernel.configuration import (
    KernelConfiguration,
)
from apps.datavionos.kernel.environment import (
    KernelEnvironment,
)


@dataclass(
    slots=True,
)
class Kernel:
    """
    Primary entry point for DatavionOS.

    Coordinates the application host,
    runtime, and environment.
    """

    application: KernelApplication

    configuration: KernelConfiguration

    environment: KernelEnvironment = field(
        default_factory=KernelEnvironment.discover,
    )

    @classmethod
    async def create(
        cls,
        configuration: KernelConfiguration | None = None,
    ) -> Kernel:
        """
        Create a new DatavionOS kernel.
        """

        configuration = configuration or KernelConfiguration()

        application = await KernelApplication.create(
            configuration,
        )

        return cls(
            application=application,
            configuration=configuration,
            environment=KernelEnvironment.discover(),
        )

    async def initialize(
        self,
    ) -> None:
        """
        Initialize the kernel.
        """

        await self.application.initialize()

    async def start(
        self,
    ) -> None:
        """
        Start the kernel.
        """

        await self.application.start()

    async def stop(
        self,
    ) -> None:
        """
        Stop the kernel.
        """

        await self.application.stop()

    async def restart(
        self,
    ) -> None:
        """
        Restart the kernel.
        """

        await self.application.restart()

    async def dispose(
        self,
    ) -> None:
        """
        Dispose the kernel.
        """

        await self.application.dispose()

    @property
    def runtime(
        self,
    ):
        """
        Runtime coordinator.
        """

        return self.application.runtime

    @property
    def provider(
        self,
    ):
        """
        Dependency injection provider.
        """

        return self.application.provider

    @property
    def state(
        self,
    ):
        """
        Current kernel state.
        """

        return self.application.state

    @property
    def is_running(
        self,
    ) -> bool:
        """
        Whether the kernel is running.
        """

        return self.application.is_running

    async def health(
        self,
    ):
        """
        Return the kernel health status.
        """

        return await self.application.health()

    def __repr__(
        self,
    ) -> str:
        return (
            "Kernel("
            f"state={self.state.value}, "
            f"environment={self.environment.environment})"
        )


__all__ = [
    "Kernel",
]
