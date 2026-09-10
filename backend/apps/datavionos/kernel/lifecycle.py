"""
DatavionOS Kernel Lifecycle.

The kernel lifecycle intentionally uses capability-based
service contracts instead of depending on a concrete
dependency-injection container.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from inspect import isawaitable
from typing import Any

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
    Coordinates the lifecycle of runtime services.

    Lifecycle capabilities are detected by method presence:

    - initialize / initialize_async
    - start
    - stop
    - dispose / dispose_async

    This keeps the kernel independent from the legacy
    dependency-injection container and its lifecycle ABCs.
    """

    state: LifecycleState = LifecycleState.CREATED

    async def initialize(
        self,
        services: list[object],
    ) -> None:
        """
        Initialize runtime services.

        Async initialization is preferred when both synchronous
        and asynchronous initialization methods are available.
        """

        self._ensure_state(
            allowed=(
                LifecycleState.CREATED,
                LifecycleState.STOPPED,
            ),
            operation="initialize",
        )

        self.state = LifecycleState.INITIALIZING

        try:
            for service in services:
                await self._initialize_service(
                    service,
                )

            self.state = LifecycleState.INITIALIZED

        except Exception as exc:
            self.state = LifecycleState.CREATED

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

        self._ensure_state(
            allowed=(
                LifecycleState.INITIALIZED,
                LifecycleState.STOPPED,
            ),
            operation="start",
        )

        self.state = LifecycleState.STARTING

        try:
            for service in services:
                await self._invoke(
                    service,
                    "start",
                )

            self.state = LifecycleState.RUNNING

        except Exception as exc:
            self.state = LifecycleState.INITIALIZED

            raise StartupError(
                "Kernel startup failed.",
            ) from exc

    async def stop(
        self,
        services: list[object],
    ) -> None:
        """
        Stop runtime services in reverse order.
        """

        if self.state not in (
            LifecycleState.RUNNING,
            LifecycleState.STARTING,
        ):
            return

        self.state = LifecycleState.STOPPING

        try:
            for service in reversed(
                services,
            ):
                await self._invoke(
                    service,
                    "stop",
                )

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
        Dispose runtime services in reverse order.

        Async disposal is preferred when both synchronous and
        asynchronous disposal methods are available.
        """

        if self.state is LifecycleState.DISPOSED:
            return

        self.state = LifecycleState.DISPOSING

        try:
            for service in reversed(
                services,
            ):
                await self._dispose_service(
                    service,
                )

            self.state = LifecycleState.DISPOSED

        except Exception as exc:
            raise ShutdownError(
                "Kernel disposal failed.",
            ) from exc

    async def _initialize_service(
        self,
        service: object,
    ) -> None:
        """
        Initialize a single service.

        Prefer initialize_async() when available.
        """

        initialize_async = getattr(
            service,
            "initialize_async",
            None,
        )

        if callable(
            initialize_async,
        ):
            result = initialize_async()

            if isawaitable(result):
                await result

            return

        initialize = getattr(
            service,
            "initialize",
            None,
        )

        if callable(
            initialize,
        ):
            result = initialize()

            if isawaitable(result):
                await result

    async def _dispose_service(
        self,
        service: object,
    ) -> None:
        """
        Dispose a single service.

        Prefer dispose_async() when available.
        """

        dispose_async = getattr(
            service,
            "dispose_async",
            None,
        )

        if callable(
            dispose_async,
        ):
            result = dispose_async()

            if isawaitable(result):
                await result

            return

        dispose = getattr(
            service,
            "dispose",
            None,
        )

        if callable(
            dispose,
        ):
            result = dispose()

            if isawaitable(result):
                await result

    async def _invoke(
        self,
        service: object,
        method_name: str,
    ) -> None:
        """
        Invoke an optional lifecycle method.

        Both synchronous and asynchronous implementations are
        supported.
        """

        method: Any = getattr(
            service,
            method_name,
            None,
        )

        if not callable(
            method,
        ):
            return

        result = method()

        if isawaitable(result):
            await result

    def _ensure_state(
        self,
        *,
        allowed: tuple[LifecycleState, ...],
        operation: str,
    ) -> None:
        """
        Validate that a lifecycle operation is legal.
        """

        if self.state in allowed:
            return

        allowed_values = ", ".join(
            state.value
            for state in allowed
        )

        raise StartupError(
            (
                f"Cannot {operation} runtime from state "
                f"'{self.state.value}'. "
                f"Expected one of: {allowed_values}."
            ),
        )

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
        return (
            f"KernelLifecycle("
            f"state={self.state.value})"
        )


__all__ = [
    "LifecycleState",
    "KernelLifecycle",
]
