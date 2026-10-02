"""
Event registry for DatavionOS.

Maintains the mapping between event names and their handlers.

The registry is framework-level infrastructure.

Business applications register their handlers during application
startup.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from apps.common.events.exceptions import (
    EventAlreadyRegisteredError,
)
from apps.common.events.handlers import (
    BaseEventHandler,
)
from apps.common.events.types import (
    EventName,
)


class EventRegistry:
    """
    Central event handler registry.

    Supports multiple handlers per event.

    Example:

        patient.registered

            |
            +-- AuditHandler
            +-- NotificationHandler
            +-- AnalyticsHandler
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize empty registry.
        """

        self._handlers: dict[
            EventName,
            list[type[BaseEventHandler]],
        ] = defaultdict(list)

    def register(
        self,
        event_name: EventName,
        handler: type[BaseEventHandler],
    ) -> None:
        """
        Register an event handler.

        Raises:
            EventAlreadyRegisteredError:
                If the same handler is registered twice.
        """

        handlers = self._handlers[event_name]

        if handler in handlers:
            raise EventAlreadyRegisteredError(
                (f"Handler {handler.__name__} is already registered for {event_name}."),
            )

        handlers.append(
            handler,
        )

    def unregister(
        self,
        event_name: EventName,
        handler: type[BaseEventHandler],
    ) -> None:
        """
        Remove a handler from an event.
        """

        handlers = self._handlers.get(
            event_name,
            [],
        )

        if handler in handlers:
            handlers.remove(
                handler,
            )

    def get_handlers(
        self,
        event_name: EventName,
    ) -> tuple[type[BaseEventHandler], ...]:
        """
        Return handlers registered for an event.
        """

        return tuple(
            self._handlers.get(
                event_name,
                [],
            ),
        )

    def has_handlers(
        self,
        event_name: EventName,
    ) -> bool:
        """
        Check whether an event has handlers.
        """

        return bool(
            self._handlers.get(
                event_name,
            ),
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all registrations.
        """

        self._handlers.clear()

    def events(
        self,
    ) -> Iterable[EventName]:
        """
        Return registered event names.
        """

        return self._handlers.keys()


event_registry = EventRegistry()


__all__: tuple[str, ...] = (
    "EventRegistry",
    "event_registry",
)
