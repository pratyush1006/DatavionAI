"""
DatavionOS lifecycle framework.

Provides the runtime lifecycle state machine,
base component abstraction, lifecycle manager,
and lifecycle event definitions.
"""

from apps.datavionos.lifecycle.base import (
    LifecycleComponent,
)
from apps.datavionos.lifecycle.events import (
    EVENT_TYPES,
    FailedEvent,
    InitializedEvent,
    LifecycleEvent,
    PausedEvent,
    RestartedEvent,
    ResumedEvent,
    StartedEvent,
    StoppedEvent,
    TerminatedEvent,
)
from apps.datavionos.lifecycle.manager import (
    LifecycleManager,
)
from apps.datavionos.lifecycle.state import (
    DEFAULT_TRANSITIONS,
    LifecycleState,
    LifecycleTransition,
    allowed_transitions,
    can_transition,
    is_running_state,
    is_stopped_state,
    is_terminal_state,
    transition_identifiers,
)

__all__ = [
    "LifecycleComponent",
    "LifecycleManager",
    "LifecycleState",
    "LifecycleTransition",
    "LifecycleEvent",
    "InitializedEvent",
    "StartedEvent",
    "PausedEvent",
    "ResumedEvent",
    "StoppedEvent",
    "RestartedEvent",
    "FailedEvent",
    "TerminatedEvent",
    "DEFAULT_TRANSITIONS",
    "EVENT_TYPES",
    "allowed_transitions",
    "can_transition",
    "is_running_state",
    "is_stopped_state",
    "is_terminal_state",
    "transition_identifiers",
]
