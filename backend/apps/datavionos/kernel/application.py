"""
DatavionOS Kernel Application.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.kernel.bootstrap import (
    KernelBootstrap,
)
from apps.datavionos.kernel.configuration import (
    KernelConfiguration,
)
from apps.datavionos.kernel.runtime import (
    KernelRuntime,
)


@dataclass(
    slots=True,
)
class KernelApplication:
    """
    Hosted DatavionOS application.

    Acts as the high-level host that
    owns the runtime.
    """

    runtime: KernelRuntime

    @classmethod
    async def create(
        cls,
        configuration: KernelConfiguration,
    ) -> KernelApplication:
        """
        Build and bootstrap the
        DatavionOS application.
        """

        bootstrap = KernelBootstrap.create(
            configuration,
        )

        provider = await bootstrap.bootstrap()

        runtime = KernelRuntime(
            provider=provider,
        )

        return cls(
            runtime=runtime,
        )

    async def initialize(
        self,
    ) -> None:
        """
        Initialize the runtime.
        """

        await self.runtime.initialize()

    async def start(
        self,
    ) -> None:
        """
        Start the runtime.
        """

        await self.runtime.start()

    async def stop(
        self,
    ) -> None:
        """
        Stop the runtime.
        """

        await self.runtime.stop()

    async def dispose(
        self,
    ) -> None:
        """
        Dispose the runtime.
        """

        await self.runtime.dispose()

    async def restart(
        self,
    ) -> None:
        """
        Restart the runtime.
        """

        await self.runtime.restart()

    @property
    def provider(
        self,
    ):
        """
        Runtime service provider.
        """

        return self.runtime.provider

    @property
    def state(
        self,
    ):
        """
        Current runtime state.
        """

        return self.runtime.state

    @property
    def is_running(
        self,
    ) -> bool:
        """
        Whether the runtime is running.
        """

        return self.runtime.is_running

    async def health(
        self,
    ):
        """
        Return runtime health.
        """

        return await self.runtime.health_status()

    def __repr__(
        self,
    ) -> str:
        return f"KernelApplication(state={self.state.value})"


__all__ = [
    "KernelApplication",
]
