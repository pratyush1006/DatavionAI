"""
Event handler contracts.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from apps.core.events.base import DomainEvent


@runtime_checkable
class EventHandler(Protocol):
    """
    Base protocol for synchronous event handlers.
    """

    def handle(
        self,
        event: DomainEvent,
    ) -> None: ...


@runtime_checkable
class AsyncEventHandler(Protocol):
    """
    Base protocol for asynchronous event handlers.
    """

    async def handle(
        self,
        event: DomainEvent,
    ) -> None: ...


__all__: tuple[str, ...] = (
    "AsyncEventHandler",
    "EventHandler",
)
