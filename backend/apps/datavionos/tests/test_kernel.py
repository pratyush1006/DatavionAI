"""
Unit tests for the DatavionOS kernel.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress

import pytest

from apps.datavionos.exceptions import KernelError
from apps.datavionos.kernel import (
    KernelLifecycle,
    KernelManager,
    KernelState,
    KernelStatus,
)


def test_initial_kernel_state() -> None:
    """
    Verify the default kernel state.
    """
    state = KernelState()

    assert state.status is KernelStatus.CREATED
    assert state.started_at is None
    assert state.stopped_at is None
    assert state.error is None
    assert state.metadata == {}


def test_valid_lifecycle_transitions() -> None:
    """
    Verify valid lifecycle transitions.
    """
    lifecycle = KernelLifecycle()

    assert lifecycle.can_transition(
        KernelStatus.CREATED,
        KernelStatus.INITIALIZING,
    )

    assert lifecycle.can_transition(
        KernelStatus.RUNNING,
        KernelStatus.STOPPING,
    )


def test_invalid_lifecycle_transition() -> None:
    """
    Invalid transitions should raise KernelError.
    """
    lifecycle = KernelLifecycle()

    with pytest.raises(KernelError):
        lifecycle.validate_transition(
            current=KernelStatus.CREATED,
            target=KernelStatus.RUNNING,
        )


def test_kernel_manager_initialize() -> None:
    """
    Verify kernel initialization.
    """
    manager = KernelManager()

    state = manager.initialize()

    assert state.status is KernelStatus.INITIALIZED
    assert manager.status is KernelStatus.INITIALIZED


def test_kernel_manager_start() -> None:
    """
    Verify kernel startup.
    """
    manager = KernelManager()

    manager.initialize()

    state = manager.start()

    assert state.status is KernelStatus.RUNNING
    assert state.started_at is not None
    assert manager.status is KernelStatus.RUNNING


def test_kernel_manager_stop() -> None:
    """
    Verify kernel shutdown.
    """
    manager = KernelManager()

    manager.initialize()
    manager.start()

    state = manager.stop()

    assert state.status is KernelStatus.STOPPED
    assert state.stopped_at is not None


def test_kernel_failure() -> None:
    """
    Verify kernel failure handling.
    """
    manager = KernelManager()

    state = manager.fail(
        message="Unexpected failure",
    )

    assert state.status is KernelStatus.FAILED
    assert state.error == "Unexpected failure"


def test_kernel_reset() -> None:
    """
    Verify kernel reset restores the initial state.
    """
    manager = KernelManager()

    manager.initialize()
    manager.start()

    state = manager.reset()

    assert state.status is KernelStatus.CREATED
    assert state.started_at is None
    assert state.stopped_at is None
    assert state.error is None
    assert state.metadata == {}


def test_snapshot_generation() -> None:
    """
    Verify snapshot generation.
    """
    manager = KernelManager()

    snapshot = manager.snapshot()

    assert snapshot["status"] == KernelStatus.CREATED.value
    assert "generated_at" in snapshot
    assert "metadata" in snapshot
    assert isinstance(snapshot["metadata"], dict)


def test_snapshot_returns_metadata_copy() -> None:
    """
    Snapshot metadata should be a defensive copy.
    """
    manager = KernelManager()

    manager.initialize(
        metadata={
            "tenant": "acme",
        },
    )

    snapshot = manager.snapshot()

    snapshot["metadata"]["tenant"] = "modified"

    assert manager.state.metadata["tenant"] == "acme"


def test_state_is_immutable_after_transition() -> None:
    """
    Every transition should produce a new immutable state object.
    """
    manager = KernelManager()

    initial_state = manager.state

    manager.initialize()

    assert manager.state is not initial_state


def test_initialize_with_metadata() -> None:
    """
    Verify metadata is stored during initialization.
    """
    manager = KernelManager()

    manager.initialize(
        metadata={
            "environment": "development",
            "version": "1.0.0",
        },
    )

    assert manager.state.metadata["environment"] == "development"
    assert manager.state.metadata["version"] == "1.0.0"


def test_thread_safe_initialize() -> None:
    """
    Verify concurrent initialization does not corrupt state.
    """
    manager = KernelManager()

    def initialize() -> None:
        with suppress(KernelError):
            manager.initialize()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(initialize)
            for _ in range(4)
        ]

        for future in futures:
            future.result()

    assert manager.status in {
        KernelStatus.INITIALIZED,
        KernelStatus.INITIALIZING,
    }


def test_thread_safe_start() -> None:
    """
    Verify concurrent startup keeps the kernel consistent.
    """
    manager = KernelManager()

    manager.initialize()

    def start() -> None:
        with suppress(KernelError):
            manager.start()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(start)
            for _ in range(4)
        ]

        for future in futures:
            future.result()

    assert manager.status is KernelStatus.RUNNING
