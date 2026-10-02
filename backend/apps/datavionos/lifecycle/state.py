"""
Lifecycle state definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class LifecycleState(StrEnum):
    """
    Standard lifecycle states used throughout
    DatavionOS.
    """

    CREATED = "created"

    INITIALIZING = "initializing"

    INITIALIZED = "initialized"

    STARTING = "starting"

    RUNNING = "running"

    PAUSING = "pausing"

    PAUSED = "paused"

    RESUMING = "resuming"

    STOPPING = "stopping"

    STOPPED = "stopped"

    RESTARTING = "restarting"

    SHUTTING_DOWN = "shutting_down"

    TERMINATED = "terminated"

    FAILED = "failed"


@dataclass(
    frozen=True,
    slots=True,
)
class LifecycleTransition:
    """
    Represents a lifecycle state transition.
    """

    source: LifecycleState

    destination: LifecycleState

    description: str = ""

    @property
    def identifier(self) -> str:
        """
        Unique transition identifier.
        """

        return f"{self.source.value}->{self.destination.value}"

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"{self.source.value!r} -> "
            f"{self.destination.value!r})"
        )


DEFAULT_TRANSITIONS: tuple[LifecycleTransition, ...] = (
    LifecycleTransition(
        LifecycleState.CREATED,
        LifecycleState.INITIALIZING,
    ),
    LifecycleTransition(
        LifecycleState.INITIALIZING,
        LifecycleState.INITIALIZED,
    ),
    LifecycleTransition(
        LifecycleState.INITIALIZED,
        LifecycleState.STARTING,
    ),
    LifecycleTransition(
        LifecycleState.STARTING,
        LifecycleState.RUNNING,
    ),
    LifecycleTransition(
        LifecycleState.RUNNING,
        LifecycleState.PAUSING,
    ),
    LifecycleTransition(
        LifecycleState.PAUSING,
        LifecycleState.PAUSED,
    ),
    LifecycleTransition(
        LifecycleState.PAUSED,
        LifecycleState.RESUMING,
    ),
    LifecycleTransition(
        LifecycleState.RESUMING,
        LifecycleState.RUNNING,
    ),
    LifecycleTransition(
        LifecycleState.RUNNING,
        LifecycleState.STOPPING,
    ),
    LifecycleTransition(
        LifecycleState.STOPPING,
        LifecycleState.STOPPED,
    ),
    LifecycleTransition(
        LifecycleState.STOPPED,
        LifecycleState.RESTARTING,
    ),
    LifecycleTransition(
        LifecycleState.RESTARTING,
        LifecycleState.STARTING,
    ),
    LifecycleTransition(
        LifecycleState.RUNNING,
        LifecycleState.FAILED,
    ),
    LifecycleTransition(
        LifecycleState.FAILED,
        LifecycleState.TERMINATED,
    ),
)

_ALLOWED_TRANSITIONS: dict[
    LifecycleState,
    frozenset[LifecycleState],
] = {state: frozenset() for state in LifecycleState}

for transition in DEFAULT_TRANSITIONS:
    _ALLOWED_TRANSITIONS[transition.source] = _ALLOWED_TRANSITIONS[
        transition.source
    ] | {
        transition.destination,
    }


def allowed_transitions(
    state: LifecycleState,
) -> frozenset[LifecycleState]:
    """
    Return all allowed destination states.
    """

    return _ALLOWED_TRANSITIONS.get(
        state,
        frozenset(),
    )


def can_transition(
    source: LifecycleState,
    destination: LifecycleState,
) -> bool:
    """
    Determine whether a transition is valid.
    """

    return destination in allowed_transitions(
        source,
    )


def is_terminal_state(
    state: LifecycleState,
) -> bool:
    """
    Whether the state is terminal.
    """

    return state in {
        LifecycleState.TERMINATED,
        LifecycleState.FAILED,
    }


def is_running_state(
    state: LifecycleState,
) -> bool:
    """
    Whether the component is operational.
    """

    return state in {
        LifecycleState.RUNNING,
        LifecycleState.RESUMING,
    }


def is_stopped_state(
    state: LifecycleState,
) -> bool:
    """
    Whether the component is stopped.
    """

    return state in {
        LifecycleState.STOPPED,
        LifecycleState.TERMINATED,
    }


def transition_identifiers() -> tuple[
    str,
    ...,
]:
    """
    Return every transition identifier.
    """

    return tuple(transition.identifier for transition in DEFAULT_TRANSITIONS)


__all__ = [
    "LifecycleState",
    "LifecycleTransition",
    "DEFAULT_TRANSITIONS",
    "allowed_transitions",
    "can_transition",
    "is_terminal_state",
    "is_running_state",
    "is_stopped_state",
    "transition_identifiers",
]
