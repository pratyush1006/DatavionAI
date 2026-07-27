"""
Event dispatcher for DatavionOS.

Provides the execution engine for publishing events to registered
handlers.

The dispatcher is framework-level infrastructure.

Business logic belongs inside event handlers.
"""

from __future__ import annotations

from typing import Any

from apps.common.events.exceptions import (
    EventDispatchError,
    EventHandlerError,
)
from apps.common.events.models import (
    Event,
    EventResult,
)
from apps.common.events.registry import (
    event_registry,
)


class EventDispatcher:
    """
    Dispatch events to registered handlers.

    Flow:

        Event
          |
          v
        Dispatcher
          |
          v
        Registry
          |
          v
        Handlers
    """

    def dispatch(
        self,
        event: Event,
    ) -> EventResult:
        """
        Dispatch an event synchronously.

        Args:
            event:
                Event instance to dispatch.

        Returns:
            EventResult containing execution details.

        Raises:
            EventDispatchError:
                When dispatching fails.
        """

        handlers = event_registry.get_handlers(
            event.name,
        )

        executed = 0

        try:
            for handler_class in handlers:
                handler = handler_class()

                self._execute_handler(
                    handler,
                    event,
                )

                executed += 1

        except Exception as exc:
            raise EventDispatchError(
                (f"Failed dispatching event {event.name}: {exc}"),
            ) from exc

        return EventResult(
            event_id=event.event_id,
            handled=bool(
                handlers,
            ),
            handlers_executed=executed,
        )

    def _execute_handler(
        self,
        handler: Any,
        event: Event,
    ) -> None:
        """
        Execute an event handler.
        """

        try:
            handler.handle(
                event,
            )

        except Exception as exc:
            raise EventHandlerError(
                (
                    f"Handler "
                    f"{handler.__class__.__name__} "
                    f"failed for event "
                    f"{event.name}: {exc}"
                ),
            ) from exc


event_dispatcher = EventDispatcher()


def dispatch_event(
    event: Event,
) -> EventResult:
    """
    Convenience function for dispatching events.
    """

    return event_dispatcher.dispatch(
        event,
    )


__all__: tuple[str, ...] = (
    "EventDispatcher",
    "dispatch_event",
    "event_dispatcher",
)
