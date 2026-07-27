"""
Message queue contracts.
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
class MessageQueue(
    Protocol,
):
    """
    Durable message queue.
    """

    async def enqueue(
        self,
        message: Message,
    ) -> None:
        """
        Add a message to the queue.
        """

    async def dequeue(
        self,
    ) -> Message | None:
        """
        Remove and return the next message.
        """

    async def peek(
        self,
    ) -> Message | None:
        """
        Return the next message without removing it.
        """

    async def acknowledge(
        self,
        message: Message,
    ) -> None:
        """
        Mark a message as successfully processed.
        """

    async def reject(
        self,
        message: Message,
    ) -> None:
        """
        Reject a message for retry or dead-letter handling.
        """

    async def size(
        self,
    ) -> int:
        """
        Return the current queue size.
        """

    async def is_empty(
        self,
    ) -> bool:
        """
        Determine whether the queue is empty.
        """


__all__ = [
    "MessageQueue",
]
