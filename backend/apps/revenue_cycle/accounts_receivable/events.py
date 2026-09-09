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
        """Initialize an Accounts Receivable event."""

        super().__init__(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )


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
