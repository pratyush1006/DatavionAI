"""Domain events for Revenue Cycle cross-module integration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent, publish_after_commit


class CrossModuleIntegrationEvent(DomainEvent):
    """Represent a cross-module Revenue Cycle integration event."""

    def __init__(
        self,
        *,
        event_type: str,
        aggregate_id: UUID,
        payload: dict[str, Any],
    ) -> None:
        """Initialize an integration domain event."""

        super().__init__(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )


def publish_integration_event(
    *,
    event_type: str,
    aggregate_id: UUID,
    payload: dict[str, Any],
) -> None:
    """Publish an integration event after the current transaction commits."""

    publish_after_commit(
        CrossModuleIntegrationEvent(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )
    )


__all__ = (
    "CrossModuleIntegrationEvent",
    "publish_integration_event",
)
