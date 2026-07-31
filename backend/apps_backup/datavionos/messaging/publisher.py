"""
Message publisher contracts.
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
class MessagePublisher(
    Protocol,
):
    """
    Publishes messages.
    """

    async def publish(
        self,
        message: Message,
    ) -> None:
        """
        Publish a message.
        """


@runtime_checkable
class BatchMessagePublisher(
    Protocol,
):
    """
    Publishes multiple messages.
    """

    async def publish_batch(
        self,
        messages: tuple[Message, ...],
    ) -> None:
        """
        Publish multiple messages.
        """


__all__ = [
    "BatchMessagePublisher",
    "MessagePublisher",
]
