"""
Domain aggregate root abstractions.
"""

from __future__ import annotations

from typing import TypeVar

from apps.domain.common.domain_event import DomainEvent
from apps.domain.common.entity import Entity

TIdentity = TypeVar("TIdentity")


class AggregateRoot[TIdentity](
    Entity[TIdentity],
):
    """
    Base class for aggregate roots.
    """

    def __init__(
        self,
        identity: TIdentity,
    ) -> None:
        super().__init__(identity)

        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(
        self,
    ) -> tuple[DomainEvent, ...]:
        """
        Return pending domain events.
        """
        return tuple(self._domain_events)

    def add_domain_event(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Register a domain event.
        """
        self._domain_events.append(event)

    def remove_domain_event(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Remove a domain event.
        """
        self._domain_events.remove(event)

    def clear_domain_events(
        self,
    ) -> None:
        """
        Clear all pending domain events.
        """
        self._domain_events.clear()

    def has_domain_events(
        self,
    ) -> bool:
        """
        Determine whether pending events exist.
        """
        return bool(self._domain_events)
