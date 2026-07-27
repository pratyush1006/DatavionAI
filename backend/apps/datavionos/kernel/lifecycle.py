"""
DatavionOS Kernel Lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from apps.datavionos.container.service import (
    AsyncDisposable,
    AsyncInitializable,
    Disposable,
    Initializable,
    Startable,
    Stoppable,
)
from apps.datavionos.kernel.exceptions import (
    ShutdownError,
    StartupError,
)


@unique
class LifecycleState(
    Enum,
):
    """
    Runtime lifecycle states.
    """

    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    DISPOSING = "disposing"
    DISPOSED = "disposed"

    def __str__(
        self,
    ) -> str:
        return self.value


@dataclass(
    slots=True,
)
class KernelLifecycle:
    """
    Coordinates the lifecycle of
    runtime services.
    """

    state: LifecycleState = LifecycleState.CREATED

    async def initialize(
        self,
        services: list[object],
    ) -> None:
        """
        Initialize runtime services.
        """

        self.state = LifecycleState.INITIALIZING

        try:
            for service in services:
                if isinstance(
                    service,
                    Initializable,
                ):
                    service.initialize()

                if isinstance(
                    service,
                    AsyncInitializable,
                ):
                    await service.initialize()

            self.state = LifecycleState.INITIALIZED

        except Exception as exc:
            raise StartupError(
                "Kernel initialization failed.",
            ) from exc

    async def start(
        self,
        services: list[object],
    ) -> None:
        """
        Start runtime services.
        """

        self.state = LifecycleState.STARTING

        try:
            for service in services:
                if isinstance(
                    service,
                    Startable,
                ):
                    service.start()

            self.state = LifecycleState.RUNNING

        except Exception as exc:
            raise StartupError(
                "Kernel startup failed.",
            ) from exc

    async def stop(
        self,
        services: list[object],
    ) -> None:
        """
        Stop runtime services.
        """

        self.state = LifecycleState.STOPPING

        try:
            for service in reversed(
                services,
            ):
                if isinstance(
                    service,
                    Stoppable,
                ):
                    service.stop()

            self.state = LifecycleState.STOPPED

        except Exception as exc:
            raise ShutdownError(
                "Kernel shutdown failed.",
            ) from exc

    async def dispose(
        self,
        services: list[object],
    ) -> None:
        """
        Dispose runtime services.
        """

        self.state = LifecycleState.DISPOSING

        try:
            for service in reversed(
                services,
            ):
                if isinstance(
                    service,
                    Disposable,
                ):
                    service.dispose()

                if isinstance(
                    service,
                    AsyncDisposable,
                ):
                    await service.dispose()

            self.state = LifecycleState.DISPOSED

        except Exception as exc:
            raise ShutdownError(
                "Kernel disposal failed.",
            ) from exc

    @property
    def is_running(
        self,
    ) -> bool:
        """
        Whether the runtime is active.
        """

        return self.state is LifecycleState.RUNNING

    @property
    def is_stopped(
        self,
    ) -> bool:
        """
        Whether the runtime has stopped.
        """

        return self.state in (
            LifecycleState.STOPPED,
            LifecycleState.DISPOSED,
        )

    def __repr__(
        self,
    ) -> str:
        return f"KernelLifecycle(state={self.state.value})"


__all__ = [
    "LifecycleState",
    "KernelLifecycle",
]
