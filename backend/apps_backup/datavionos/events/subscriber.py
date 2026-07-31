"""
DatavionOS Event Subscriber Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from apps.datavionos.events.event import (
    Event,
)


class EventSubscriber(
    ABC,
):
    """
    Transport-agnostic event subscriber.

    Implementations may consume events
    from:

    - Kafka
    - RabbitMQ
    - Azure Service Bus
    - AWS EventBridge
    - Google Pub/Sub
    - EventStoreDB
    """

    @property
    def subscriber_name(
        self,
    ) -> str:
        """
        Subscriber name.
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
    def consumer_group(
        self,
    ) -> str:
        """
        Consumer group identifier.
        """

        return "default"

    @property
    def supports_batch(
        self,
    ) -> bool:
        """
        Whether batch consumption is supported.
        """

        return True

    @property
    def supports_checkpointing(
        self,
    ) -> bool:
        """
        Whether offsets/checkpoints
        are supported.
        """

        return False

    @property
    def supports_dead_letter(
        self,
    ) -> bool:
        """
        Whether dead-letter queues
        are supported.
        """

        return False

    @property
    def supports_retry(
        self,
    ) -> bool:
        """
        Whether retry is supported.
        """

        return True

    @abstractmethod
    def subscribe(
        self,
    ) -> None:
        """
        Begin consuming events.
        """

    @abstractmethod
    def unsubscribe(
        self,
    ) -> None:
        """
        Stop consuming events.
        """

    @abstractmethod
    def receive(
        self,
    ) -> Event | None:
        """
        Receive the next event.

        Returns None if no event is
        currently available.
        """

    @abstractmethod
    def receive_many(
        self,
        max_events: int,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Receive multiple events.
        """

    @abstractmethod
    def acknowledge(
        self,
        event: Event,
    ) -> None:
        """
        Acknowledge successful processing.
        """

    @abstractmethod
    def reject(
        self,
        event: Event,
        *,
        requeue: bool = False,
    ) -> None:
        """
        Reject an event.
        """

    def __iter__(
        self,
    ) -> Iterable[Event,]:
        """
        Continuous event iterator.
        """

        while True:
            event = self.receive()

            if event is None:
                break

            yield event

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.subscriber_name}("
            f"transport={self.transport!r}, "
            f"group={self.consumer_group!r})"
        )


__all__ = [
    "EventSubscriber",
]
