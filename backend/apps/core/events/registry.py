"""
Event handler registry.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from apps.core.events.base import DomainEvent
from apps.core.events.handlers import EventHandler
from apps.core.events.types import EventType


class EventRegistry:
    """
    Registry for event handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[
            EventType,
            list[EventHandler],
        ] = defaultdict(list)

    def register(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Register a handler.
        """
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unregister(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Remove a handler.
        """
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    def handlers_for(
        self,
        event: DomainEvent,
    ) -> Iterable[EventHandler]:
        """
        Return handlers for an event.
        """
        return tuple(
            self._handlers.get(
                type(event),
                [],
            ),
        )

    def clear(self) -> None:
        """
        Remove all registrations.
        """
        self._handlers.clear()


registry = EventRegistry()

__all__: tuple[str, ...] = (
    "EventRegistry",
    "registry",
)
