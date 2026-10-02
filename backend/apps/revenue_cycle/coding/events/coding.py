from __future__ import annotations

"""Domain events for Revenue Cycle Coding."""

from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


class CodingCreatedEvent(DomainEvent):
    """Represent creation of a Coding record."""

    @property
    def event_type(self) -> str:
        """Return the creation event name."""

        return "revenue_cycle.coding.created"


class CodingUpdatedEvent(DomainEvent):
    """Represent an update to a Coding record."""

    @property
    def event_type(self) -> str:
        """Return the update event name."""

        return "revenue_cycle.coding.updated"


class CodingStatusChangedEvent(DomainEvent):
    """Represent a Coding lifecycle transition."""

    @property
    def event_type(self) -> str:
        """Return the status-change event name."""

        return "revenue_cycle.coding.status_changed"


class CodingCodeAssignedEvent(DomainEvent):
    """Represent assignment of a clinical or billing code."""

    @property
    def event_type(self) -> str:
        """Return the code-assignment event name."""

        return "revenue_cycle.coding.code_assigned"


class CodingDeletedEvent(DomainEvent):
    """Represent soft deletion of a Coding record."""

    @property
    def event_type(self) -> str:
        """Return the deletion event name."""

        return "revenue_cycle.coding.deleted"


class CodingRestoredEvent(DomainEvent):
    """Represent restoration of a Coding record."""

    @property
    def event_type(self) -> str:
        """Return the restoration event name."""

        return "revenue_cycle.coding.restored"


def build_coding_event(
    *,
    event_name: str,
    coding_record_id: UUID,
    organization_id: UUID,
    tenant_id: UUID,
    actor_id: UUID | None,
    metadata: dict[str, Any] | None = None,
) -> DomainEvent:
    """Build a canonical Core DomainEvent for a Coding mutation."""

    event_classes = {
        "revenue_cycle.coding.created": CodingCreatedEvent,
        "revenue_cycle.coding.updated": CodingUpdatedEvent,
        "revenue_cycle.coding.status_changed": CodingStatusChangedEvent,
        "revenue_cycle.coding.code_assigned": CodingCodeAssignedEvent,
        "revenue_cycle.coding.deleted": CodingDeletedEvent,
        "revenue_cycle.coding.restored": CodingRestoredEvent,
    }

    event_class = event_classes.get(event_name)
    if event_class is None:
        raise ValueError(f"Unsupported Coding event name: {event_name}")

    return event_class(
        tenant_id=tenant_id,
        actor_id=actor_id,
        metadata={
            "coding_record_id": str(coding_record_id),
            "organization_id": str(organization_id),
            **(metadata or {}),
        },
    )


CodingDomainEvent = DomainEvent


__all__ = (
    "CodingCodeAssignedEvent",
    "CodingCreatedEvent",
    "CodingDeletedEvent",
    "CodingDomainEvent",
    "CodingRestoredEvent",
    "CodingStatusChangedEvent",
    "CodingUpdatedEvent",
    "build_coding_event",
)
