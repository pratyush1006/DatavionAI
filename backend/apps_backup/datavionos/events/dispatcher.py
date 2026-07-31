"""
DatavionOS Event Dispatcher Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from apps.datavionos.events.event import (
    Event,
)
from apps.datavionos.events.handler import (
    EventHandler,
)


class EventDispatcher(
    ABC,
):
    """
    Dispatches events to one or more
    subscribed handlers.

    Unlike CommandDispatcher and
    QueryDispatcher, an event dispatcher
    fans out events to every registered
    handler.
    """

    @abstractmethod
    def dispatch(
        self,
        event: Event,
    ) -> int:
        """
        Dispatch an event.

        Returns
        -------
        int
            Number of handlers invoked.
        """

    @abstractmethod
    def dispatch_many(
        self,
        events: Iterable[Event],
    ) -> int:
        """
        Dispatch multiple events.

        Returns
        -------
        int
            Total number of handler
            invocations.
        """

    @abstractmethod
    def get_handlers(
        self,
        event: Event,
    ) -> tuple[
        EventHandler,
        ...,
    ]:
        """
        Retrieve handlers registered
        for the supplied event.
        """

    def __call__(
        self,
        event: Event,
    ) -> int:
        """
        Callable shortcut.
        """

        return self.dispatch(
            event,
        )


__all__ = [
    "EventDispatcher",
]
