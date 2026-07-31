"""
Messaging service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.messaging.bus import (
    MessageBus,
)
from apps.datavionos.messaging.publisher import (
    MessagePublisher,
)
from apps.datavionos.messaging.queue import (
    MessageQueue,
)
from apps.datavionos.messaging.router import (
    MessageRouter,
)
from apps.datavionos.messaging.subscriber import (
    MessageSubscriber,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MessagingServices:
    """
    Aggregate of messaging services.
    """

    bus: MessageBus

    publisher: MessagePublisher

    subscriber: MessageSubscriber

    queue: MessageQueue

    router: MessageRouter


__all__ = [
    "MessagingServices",
]
