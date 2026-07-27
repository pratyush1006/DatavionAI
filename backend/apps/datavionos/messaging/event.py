"""
Event messaging contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.messaging.message import (
    Message,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Event(
    Message,
):
    """
    Base event contract.

    An event represents something that has
    already happened.
    """


@runtime_checkable
class EventHandler(
    Protocol,
):
    """
    Handles an event.
    """

    async def handle(
        self,
        event: Event,
    ) -> None:
        """
        Handle an event.
        """


@runtime_checkable
class EventDispatcher(
    Protocol,
):
    """
    Publishes events to subscribers.
    """

    async def dispatch(
        self,
        event: Event,
    ) -> None:
        """
        Dispatch an event.
        """


__all__ = [
    "Event",
    "EventDispatcher",
    "EventHandler",
]
