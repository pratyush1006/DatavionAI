"""
DatavionOS Event Handler Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from apps.datavionos.events.event import (
    Event,
)

TEvent = TypeVar(
    "TEvent",
    bound=Event,
)


class EventHandler[TEvent: Event](
    ABC,
):
    """
    Base class for all event handlers.

    Unlike command handlers, multiple
    event handlers may subscribe to
    the same event.
    """

    @property
    @abstractmethod
    def event_type(
        self,
    ) -> type[TEvent]:
        """
        Supported event type.
        """

    @property
    def handler_name(
        self,
    ) -> str:
        """
        Handler name.
        """

        return self.__class__.__qualname__

    @property
    def priority(
        self,
    ) -> int:
        """
        Handler execution priority.

        Lower values execute first.
        """

        return 0

    @property
    def enabled(
        self,
    ) -> bool:
        """
        Whether this handler is enabled.
        """

        return True

    @property
    def asynchronous(
        self,
    ) -> bool:
        """
        Indicates whether the handler
        should execute asynchronously.

        The default event bus executes
        synchronously. Future distributed
        buses may use this hint.
        """

        return False

    @abstractmethod
    def handle(
        self,
        event: TEvent,
    ) -> None:
        """
        Process an event.
        """

    def can_handle(
        self,
        event: Event,
    ) -> bool:
        """
        Determine whether this handler
        supports the supplied event.
        """

        return isinstance(
            event,
            self.event_type,
        )

    def __call__(
        self,
        event: TEvent,
    ) -> None:
        """
        Invoke the handler.
        """

        if not self.enabled:
            return

        self.handle(
            event,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.handler_name}("
            f"event_type="
            f"{self.event_type.__qualname__}, "
            f"priority={self.priority}, "
            f"async={self.asynchronous})"
        )


__all__ = [
    "EventHandler",
]
