"""
DatavionOS Kernel Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apps.datavionos.container import (
    ServiceProvider,
)
from apps.datavionos.kernel.health import (
    KernelHealth,
)
from apps.datavionos.kernel.lifecycle import (
    KernelLifecycle,
    LifecycleState,
)


@dataclass(
    slots=True,
)
class KernelRuntime:
    """
    Coordinates the execution of the
    DatavionOS runtime.
    """

    provider: ServiceProvider

    lifecycle: KernelLifecycle = field(
        default_factory=KernelLifecycle,
    )

    health: KernelHealth = field(
        default_factory=KernelHealth,
    )

    services: list[object] = field(
        default_factory=list,
    )

    async def initialize(
        self,
    ) -> None:
        """
        Initialize runtime services.
        """

        await self.lifecycle.initialize(
            self.services,
        )

    async def start(
        self,
    ) -> None:
        """
        Start runtime services.
        """

        await self.lifecycle.start(
            self.services,
        )

    async def stop(
        self,
    ) -> None:
        """
        Stop runtime services.
        """

        await self.lifecycle.stop(
            self.services,
        )

    async def dispose(
        self,
    ) -> None:
        """
        Dispose runtime services.
        """

        await self.lifecycle.dispose(
            self.services,
        )

    async def restart(
        self,
    ) -> None:
        """
        Restart the runtime.
        """

        await self.stop()
        await self.start()

    @property
    def state(
        self,
    ) -> LifecycleState:
        """
        Current runtime state.
        """

        return self.lifecycle.state

    @property
    def is_running(
        self,
    ) -> bool:
        """
        Whether the runtime is active.
        """

        return self.lifecycle.is_running

    @property
    def is_healthy(
        self,
    ) -> bool:
        """
        Whether the runtime is healthy.
        """

        return self.health.count > 0

    async def health_status(
        self,
    ):
        """
        Return the current runtime
        health status.
        """

        return await self.health.status()

    def register_service(
        self,
        service: object,
    ) -> None:
        """
        Register a managed runtime
        service.
        """

        self.services.append(
            service,
        )

    def unregister_service(
        self,
        service: object,
    ) -> None:
        """
        Remove a managed runtime
        service.
        """

        self.services.remove(
            service,
        )

    def __repr__(
        self,
    ) -> str:
        return f"KernelRuntime(state={self.state.value}, services={len(self.services)})"


__all__ = [
    "KernelRuntime",
]
