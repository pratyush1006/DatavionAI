"""Domain events for Revenue Analytics."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent, publish_after_commit


class RevenueAnalyticsEvent(DomainEvent):
    """Represent a Revenue Analytics domain event."""

    def __init__(
        self,
        *,
        event_type: str,
        aggregate_id: UUID,
        payload: dict[str, Any],
    ) -> None:
        """Initialize an analytics event against the canonical DomainEvent contract."""
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
        """Return the business event type supplied by the publisher."""
        return self._business_event_type


def publish_revenue_analytics_event(
    *,
    event_type: str,
    aggregate_id: UUID,
    payload: dict[str, Any],
) -> None:
    """Publish an analytics event after transaction commit."""

    publish_after_commit(
        RevenueAnalyticsEvent(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )
    )


__all__ = ("RevenueAnalyticsEvent", "publish_revenue_analytics_event")
