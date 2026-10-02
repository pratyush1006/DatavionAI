"""
Unit tests for the canonical DatavionOS kernel runtime.
"""

from __future__ import annotations

import asyncio

from apps.datavionos.kernel import (
    KernelLifecycle,
    KernelRuntime,
    LifecycleState,
)


def test_kernel_lifecycle_initial_state() -> None:
    """The lifecycle starts in CREATED."""
    lifecycle = KernelLifecycle()
    assert lifecycle.state is LifecycleState.CREATED
    assert lifecycle.is_running is False
    assert lifecycle.is_stopped is False


def test_kernel_lifecycle_initialize_start_stop() -> None:
    """The canonical lifecycle can initialize, start and stop services."""
    lifecycle = KernelLifecycle()

    async def exercise() -> None:
        await lifecycle.initialize([])
        assert lifecycle.state is LifecycleState.INITIALIZED
        await lifecycle.start([])
        assert lifecycle.state is LifecycleState.RUNNING
        assert lifecycle.is_running is True
        await lifecycle.stop([])
        assert lifecycle.state is LifecycleState.STOPPED
        assert lifecycle.is_stopped is True

    asyncio.run(exercise())


def test_kernel_runtime_delegates_lifecycle() -> None:
    """KernelRuntime delegates lifecycle operations to KernelLifecycle."""
    runtime = KernelRuntime()

    async def exercise() -> None:
        await runtime.initialize()
        assert runtime.state is LifecycleState.INITIALIZED
        await runtime.start()
        assert runtime.state is LifecycleState.RUNNING
        assert runtime.is_running is True
        await runtime.stop()
        assert runtime.state is LifecycleState.STOPPED

    asyncio.run(exercise())
