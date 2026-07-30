"""
SaaS Billing domain event dispatcher.

Responsible for:

- Publishing domain events
- Registering event handlers
- Dispatching events asynchronously later

Architecture:

Service
    |
Workflow
    |
Event Dispatcher
    |
Domain Event
    |
Handlers
    |
Audit
Notification
Analytics
Automation
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from .base import DomainEvent

EventHandler = Callable[
    [DomainEvent],
    None,
]


class EventDispatcher:
    """
    Enterprise domain event dispatcher.

    In-memory dispatcher foundation.

    Can later be replaced with:

    - Celery
    - Redis Streams
    - Kafka
    - RabbitMQ
    """

    _handlers: dict[
        type[DomainEvent],
        list[EventHandler],
    ] = defaultdict(list)

    @classmethod
    def register(
        cls,
        event_type: type[DomainEvent],
        handler: EventHandler,
    ) -> None:
        """
        Register event handler.

        Prevents duplicate handler registration
        during Django startup reload cycles.
        """

        if handler not in cls._handlers[event_type]:
            cls._handlers[event_type].append(
                handler,
            )

    @classmethod
    def dispatch(
        cls,
        event: DomainEvent,
    ) -> None:
        """
        Dispatch domain event.
        """

        handlers = cls._handlers.get(
            type(event),
            [],
        )

        for handler in handlers:
            handler(
                event,
            )

    @classmethod
    def registered_events(
        cls,
    ) -> dict[str, int]:
        """
        Return registered event counts.

        Useful for:

        - Health checks
        - Debugging
        - Automated tests
        """

        return {
            event.__name__: len(
                handlers,
            )
            for event, handlers in cls._handlers.items()
        }

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Clear registered handlers.

        Mainly used for:

        - Tests
        - Development
        """

        cls._handlers.clear()


__all__ = [
    "EventDispatcher",
]
