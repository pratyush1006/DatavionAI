"""
Event dispatcher.
"""

from __future__ import annotations

import logging

from apps.core.events.base import DomainEvent
from apps.core.events.exceptions import HandlerExecutionError
from apps.core.events.registry import registry

logger = logging.getLogger(__name__)


class EventDispatcher:
    """
    Dispatches events to registered handlers.
    """

    def dispatch(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Dispatch an event.
        """
        for handler in registry.handlers_for(event):
            try:
                handler.handle(event)

            except Exception as exc:
                logger.exception(
                    "Event handler failed.",
                    extra={
                        "event": event.event_name,
                        "handler": handler.__class__.__name__,
                    },
                )

                raise HandlerExecutionError(
                    f"{handler.__class__.__name__} failed."
                ) from exc


dispatcher = EventDispatcher()

__all__: tuple[str, ...] = (
    "EventDispatcher",
    "dispatcher",
)
