"""Domain events for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent, publish_after_commit


class AREvent(DomainEvent):
    """Represent a Revenue Cycle Accounts Receivable domain event."""

    def __init__(
        self,
        *,
        event_type: str,
        aggregate_id: UUID,
        payload: dict[str, Any],
    ) -> None:
        """Initialize an AR event against the canonical DomainEvent contract."""
        super().__init__(
            metadata={
                "event_type": event_type,
                "aggregate_id": str(aggregate_id),
                "payload": payload,
            }
        )
        object.__setattr__(self, "_business_event_type", event_type)
        object.__setattr__(self, "aggregate_id", aggregate_id)
        object.__setattr__(self, "payload", payload)

    @property
    def event_type(self) -> str:
        """Return the business event type supplied by the AR publisher."""
        return self._business_event_type


def publish_ar_event(
    *,
    event_type: str,
    aggregate_id: UUID,
    payload: dict[str, Any],
) -> None:
    """Publish an AR event after the current transaction commits."""

    publish_after_commit(
        AREvent(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )
    )


__all__ = ("AREvent", "publish_ar_event")
