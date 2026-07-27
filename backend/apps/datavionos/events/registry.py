"""
DatavionOS Event Registry.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping

from apps.datavionos.events.event import (
    Event,
)
from apps.datavionos.events.exceptions import (
    DuplicateEventHandlerException,
    EventHandlerNotFoundException,
)
from apps.datavionos.events.handler import (
    EventHandler,
)


class EventRegistry:
    """
    Registry for event handlers.

    Unlike command/query registries,
    an event may have multiple handlers.
    """

    def __init__(
        self,
    ) -> None:
        self._handlers: dict[
            type[Event],
            list[EventHandler],
        ] = {}

    def register(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Register an event handler.
        """

        event_type = handler.event_type

        handlers = self._handlers.setdefault(
            event_type,
            [],
        )

        if any(type(existing) is type(handler) for existing in handlers):
            raise DuplicateEventHandlerException(
                event_type=event_type,
                handler_name=handler.handler_name,
            )

        handlers.append(
            handler,
        )

        handlers.sort(
            key=lambda item: item.priority,
        )

    def unregister(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Remove an event handler.
        """

        event_type = handler.event_type

        handlers = self._handlers.get(
            event_type,
        )

        if handlers is None:
            raise EventHandlerNotFoundException(
                event_type=event_type,
                handler_name=handler.handler_name,
            )

        try:
            handlers.remove(
                handler,
            )
        except ValueError as exc:
            raise EventHandlerNotFoundException(
                event_type=event_type,
                handler_name=handler.handler_name,
            ) from exc

        if not handlers:
            del self._handlers[event_type]

    def get_handlers(
        self,
        event: Event | type[Event],
    ) -> tuple[
        EventHandler,
        ...,
    ]:
        """
        Return handlers for an event.
        """

        event_type = (
            event
            if isinstance(
                event,
                type,
            )
            else type(
                event,
            )
        )

        return tuple(
            self._handlers.get(
                event_type,
                [],
            ),
        )

    def contains(
        self,
        handler: EventHandler,
    ) -> bool:
        """
        Determine whether a handler
        is registered.
        """

        return handler in self.get_handlers(
            handler.event_type,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all registrations.
        """

        self._handlers.clear()

    def registered_events(
        self,
    ) -> tuple[
        type[Event],
        ...,
    ]:
        """
        Return registered event types.
        """

        return tuple(
            self._handlers.keys(),
        )

    def snapshot(
        self,
    ) -> Mapping[
        type[Event],
        tuple[EventHandler, ...],
    ]:
        """
        Read-only registry snapshot.
        """

        return {
            event_type: tuple(
                handlers,
            )
            for event_type, handlers in self._handlers.items()
        }

    def __contains__(
        self,
        event_type: type[Event],
    ) -> bool:
        return event_type in self._handlers

    def __len__(
        self,
    ) -> int:
        """
        Number of registered event types.
        """

        return len(
            self._handlers,
        )

    def __iter__(
        self,
    ) -> Iterator[
        tuple[
            type[Event],
            tuple[EventHandler, ...],
        ]
    ]:
        """
        Iterate over registrations.
        """

        for (
            event_type,
            handlers,
        ) in self._handlers.items():
            yield (
                event_type,
                tuple(
                    handlers,
                ),
            )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"events={len(self)}, "
            f"handlers="
            f"{sum(len(h) for h in self._handlers.values())})"
        )


__all__ = [
    "EventRegistry",
]
