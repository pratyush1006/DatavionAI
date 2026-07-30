"""
Shared type definitions for the event framework.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from apps.core.events.base import DomainEvent

type EventType = type[DomainEvent]

type EventHandlerCallable = Callable[
    [DomainEvent],
    None,
]

type AsyncEventHandlerCallable = Callable[
    [DomainEvent],
    Awaitable[None],
]

type EventName = str

__all__: tuple[str, ...] = (
    "AsyncEventHandlerCallable",
    "EventHandlerCallable",
    "EventName",
    "EventType",
)
