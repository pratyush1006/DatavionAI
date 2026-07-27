"""
Message routing contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.messaging.command import (
    Command,
    CommandHandler,
)
from apps.datavionos.messaging.event import (
    Event,
    EventHandler,
)
from apps.datavionos.messaging.message import (
    Message,
)


@runtime_checkable
class MessageRouter(
    Protocol,
):
    """
    Resolves handlers for messages.
    """

    async def route_command(
        self,
        command: Command,
    ) -> CommandHandler | None:
        """
        Resolve the handler for a command.
        """

    async def route_event(
        self,
        event: Event,
    ) -> tuple[EventHandler, ...]:
        """
        Resolve the subscribers for an event.
        """

    async def route(
        self,
        message: Message,
    ) -> tuple[object, ...]:
        """
        Resolve handlers for a generic message.
        """


__all__ = [
    "MessageRouter",
]
