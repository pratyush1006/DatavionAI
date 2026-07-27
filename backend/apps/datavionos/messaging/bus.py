"""
Message bus contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.messaging.command import (
    Command,
)
from apps.datavionos.messaging.event import (
    Event,
)
from apps.datavionos.messaging.message import (
    Message,
)


@runtime_checkable
class MessageBus(
    Protocol,
):
    """
    Central messaging bus.
    """

    async def dispatch(
        self,
        command: Command,
    ) -> None:
        """
        Dispatch a command.
        """

    async def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event.
        """

    async def send(
        self,
        message: Message,
    ) -> None:
        """
        Send a generic message.
        """


__all__ = [
    "MessageBus",
]
