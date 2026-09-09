"""Patient Communication status_changed domain event."""

from __future__ import annotations

from typing import Any

from apps.core.events import DomainEvent


class CommunicationStatusChangedEvent(DomainEvent):
    """Represent a Patient Communication status_changed event."""

    event_name = "patient_communication.status_changed"

    def __init__(
        self,
        *,
        communication: Any,
        actor_id: Any = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the domain event."""
        super().__init__(
            aggregate_id=communication.id,
            actor_id=actor_id,
            payload=payload
            or {
                "communication_id": str(communication.id),
                "patient_id": str(communication.patient_id),
                "organization_id": str(communication.organization_id),
                "status": communication.status,
            },
        )


__all__ = ("CommunicationStatusChangedEvent",)
