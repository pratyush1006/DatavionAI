"""
DatavionOS Event Bus.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.events.context import (
    EventContext,
)
from apps.datavionos.events.dispatcher import (
    EventDispatcher,
)
from apps.datavionos.events.event import (
    Event,
)
from apps.datavionos.events.handler import (
    EventHandler,
)
from apps.datavionos.events.middleware import (
    EventMiddleware,
)
from apps.datavionos.events.registry import (
    EventRegistry,
)


class EventBus(
    EventDispatcher,
):
    """
    Default in-process event bus.
    """

    def __init__(
        self,
        registry: EventRegistry | None = None,
    ) -> None:
        self._registry = registry or EventRegistry()

        self._middleware: list[EventMiddleware] = []

    @property
    def registry(
        self,
    ) -> EventRegistry:
        """
        Event registry.
        """

        return self._registry

    def add_middleware(
        self,
        middleware: EventMiddleware,
    ) -> None:
        """
        Register middleware.
        """

        self._middleware.append(
            middleware,
        )

    def remove_middleware(
        self,
        middleware: EventMiddleware,
    ) -> None:
        """
        Remove middleware.
        """

        self._middleware.remove(
            middleware,
        )

    def dispatch(
        self,
        event: Event,
    ) -> int:
        """
        Publish an event.
        """

        handlers = self.get_handlers(
            event,
        )

        if not handlers:
            return 0

        context = EventContext(
            event=event,
        )

        for handler in handlers:
            self._invoke(
                context=context,
                handler=handler,
            )

        return len(
            handlers,
        )

    def dispatch_many(
        self,
        events: Iterable[Event,],
    ) -> int:
        """
        Publish multiple events.
        """

        published = 0

        for event in events:
            published += self.dispatch(
                event,
            )

        return published

    def get_handlers(
        self,
        event: Event,
    ) -> tuple[
        EventHandler,
        ...,
    ]:
        """
        Resolve handlers.
        """

        return self._registry.get_handlers(
            event,
        )

    def _invoke(
        self,
        *,
        context: EventContext,
        handler: EventHandler,
    ) -> None:
        """
        Execute middleware pipeline.
        """

        def execute(
            index: int,
        ) -> None:
            if index >= len(
                self._middleware,
            ):
                handler(
                    context.event,
                )
                return

            middleware = self._middleware[index]

            middleware(
                context,
                lambda: execute(
                    index + 1,
                ),
            )

        execute(
            0,
        )

    def register(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Register handler.
        """

        self._registry.register(
            handler,
        )

    def unregister(
        self,
        handler: EventHandler,
    ) -> None:
        """
        Unregister handler.
        """

        self._registry.unregister(
            handler,
        )

    def clear(
        self,
    ) -> None:
        """
        Clear registry and middleware.
        """

        self._registry.clear()
        self._middleware.clear()

    def middleware(
        self,
    ) -> tuple[
        EventMiddleware,
        ...,
    ]:
        """
        Registered middleware.
        """

        return tuple(
            self._middleware,
        )

    def __len__(
        self,
    ) -> int:
        """
        Number of registered events.
        """

        return len(
            self._registry,
        )

    def __contains__(
        self,
        event_type: type[Event,],
    ) -> bool:
        """
        Event registration lookup.
        """

        return event_type in self._registry

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"events={len(self)}, "
            f"middleware={len(self._middleware)})"
        )


__all__ = [
    "EventBus",
]
