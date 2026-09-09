"""
Core domain event publisher infrastructure.

This module provides the canonical event publisher and the transactional
after-commit publishing boundary used by DatavionAI bounded contexts.
"""

from __future__ import annotations

from collections.abc import Iterable

from django.db import transaction

from apps.core.events.base import DomainEvent
from apps.core.events.dispatcher import dispatcher


class EventPublisher:
    """Publish domain events through the canonical dispatcher."""

    def publish(
        self,
        event: DomainEvent,
    ) -> None:
        """Publish a single event immediately."""

        dispatcher.dispatch(event)

    def publish_many(
        self,
        events: Iterable[DomainEvent],
    ) -> None:
        """Publish multiple events immediately in input order."""

        for event in events:
            self.publish(event)

    def publish_after_commit(
        self,
        event: DomainEvent,
    ) -> None:
        """Publish one event only after the current transaction commits."""

        transaction.on_commit(
            lambda: self.publish(event),
        )

    def publish_many_after_commit(
        self,
        events: Iterable[DomainEvent],
    ) -> None:
        """Publish multiple events after the current transaction commits."""

        event_list = list(events)

        transaction.on_commit(
            lambda: self.publish_many(event_list),
        )


publisher = EventPublisher()


def publish_after_commit(
    event: DomainEvent,
) -> None:
    """Publish a domain event after the surrounding transaction commits."""

    publisher.publish_after_commit(event)


def publish_many_after_commit(
    events: Iterable[DomainEvent],
) -> None:
    """Publish multiple domain events after the surrounding transaction commits."""

    publisher.publish_many_after_commit(events)


__all__: tuple[str, ...] = (
    "EventPublisher",
    "publish_after_commit",
    "publish_many_after_commit",
    "publisher",
)
