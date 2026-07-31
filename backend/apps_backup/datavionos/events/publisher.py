"""
DatavionOS Event Publisher Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from apps.datavionos.events.event import (
    Event,
)
from apps.datavionos.events.result import (
    EventResult,
)


class EventPublisher(
    ABC,
):
    """
    Transport-agnostic event publisher.

    Implementations may publish events
    using:

    - In-process EventBus
    - Transactional Outbox
    - Kafka
    - RabbitMQ
    - Azure Service Bus
    - AWS EventBridge
    - Google Pub/Sub
    - EventStoreDB
    """

    @property
    def publisher_name(
        self,
    ) -> str:
        """
        Publisher name.
        """

        return self.__class__.__qualname__

    @property
    def transport(
        self,
    ) -> str:
        """
        Underlying transport.
        """

        return "in-process"

    @property
    def supports_batch(
        self,
    ) -> bool:
        """
        Indicates whether the publisher
        supports batch publication.
        """

        return True

    @property
    def supports_replay(
        self,
    ) -> bool:
        """
        Indicates whether replay
        is supported.
        """

        return False

    @property
    def supports_scheduling(
        self,
    ) -> bool:
        """
        Indicates whether delayed
        publication is supported.
        """

        return False

    @abstractmethod
    def publish(
        self,
        event: Event,
    ) -> EventResult:
        """
        Publish a single event.
        """

    @abstractmethod
    def publish_many(
        self,
        events: Iterable[Event,],
    ) -> tuple[
        EventResult,
        ...,
    ]:
        """
        Publish multiple events.
        """

    def __call__(
        self,
        event: Event,
    ) -> EventResult:
        """
        Callable shortcut.
        """

        return self.publish(
            event,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.publisher_name}("
            f"transport={self.transport!r}, "
            f"batch={self.supports_batch}, "
            f"replay={self.supports_replay}, "
            f"scheduling={self.supports_scheduling})"
        )


__all__ = [
    "EventPublisher",
]
