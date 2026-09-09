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
        """Initialize an analytics event."""

        super().__init__(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )


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
