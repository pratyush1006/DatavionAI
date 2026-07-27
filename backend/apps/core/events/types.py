"""
Shared type definitions for the event framework.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias

from apps.core.events.base import DomainEvent

EventType: TypeAlias = type[DomainEvent]

EventHandlerCallable: TypeAlias = Callable[
    [DomainEvent],
    None,
]

AsyncEventHandlerCallable: TypeAlias = Callable[
    [DomainEvent],
    Awaitable[None],
]

EventName: TypeAlias = str

__all__: tuple[str, ...] = (
    "AsyncEventHandlerCallable",
    "EventHandlerCallable",
    "EventName",
    "EventType",
)
