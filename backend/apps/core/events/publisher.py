"""
Event publisher.
"""

from __future__ import annotations

from apps.core.events.base import DomainEvent
from apps.core.events.dispatcher import dispatcher


class EventPublisher:
    """
    Publishes domain events.
    """

    def publish(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Publish a single event.
        """
        dispatcher.dispatch(event)

    def publish_many(
        self,
        events: list[DomainEvent],
    ) -> None:
        """
        Publish multiple events.
        """
        for event in events:
            self.publish(event)


publisher = EventPublisher()

__all__: tuple[str, ...] = (
    "EventPublisher",
    "publisher",
)
