"""
DatavionOS Kernel Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field

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
    Coordinates execution of the DatavionOS runtime.

    The runtime intentionally has no dependency on the legacy
    DatavionOS container abstraction.

    Runtime services are ordinary objects managed through the
    KernelLifecycle contract.
    """

    provider: list[object] = field(
        default_factory=list,
    )

    lifecycle: KernelLifecycle = field(
        default_factory=KernelLifecycle,
    )

    health: KernelHealth = field(
        default_factory=KernelHealth,
    )

    services: list[object] = field(
        default_factory=list,
    )

    def __post_init__(self) -> None:
        """Initialize managed services from the bootstrap provider."""
        if self.provider and not self.services:
            self.services.extend(self.provider)

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
        Current runtime lifecycle state.
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
        Whether the runtime has health information.
        """

        return self.health.count > 0

    async def health_status(
        self,
    ):
        """
        Return the current runtime health status.
        """

        return await self.health.status()

    def register_service(
        self,
        service: object,
    ) -> None:
        """
        Register a managed runtime service.

        Duplicate registrations are ignored.
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
        Remove a managed runtime service.
        """

        self.services.remove(
            service,
        )

    def clear_services(
        self,
    ) -> None:
        """
        Remove all registered runtime services.

        This does not dispose services. Call dispose() when
        lifecycle cleanup is required.
        """

        self.services.clear()

    def __repr__(
        self,
    ) -> str:
        return (
            f"KernelRuntime("
            f"state={self.state.value}, "
            f"services={len(self.services)})"
        )


__all__ = [
    "KernelRuntime",
]
