"""
Message subscriber contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.messaging.message import (
    Message,
)


@runtime_checkable
class MessageSubscriber(
    Protocol,
):
    """
    Receives published messages.
    """

    async def subscribe(
        self,
        message_name: str,
    ) -> None:
        """
        Subscribe to a message.
        """

    async def unsubscribe(
        self,
        message_name: str,
    ) -> None:
        """
        Remove a message subscription.
        """

    async def receive(
        self,
        message: Message,
    ) -> None:
        """
        Receive a published message.
        """


@runtime_checkable
class BatchMessageSubscriber(
    Protocol,
):
    """
    Receives batches of published messages.
    """

    async def receive_batch(
        self,
        messages: tuple[Message, ...],
    ) -> None:
        """
        Receive multiple published messages.
        """


__all__ = [
    "BatchMessageSubscriber",
    "MessageSubscriber",
]
