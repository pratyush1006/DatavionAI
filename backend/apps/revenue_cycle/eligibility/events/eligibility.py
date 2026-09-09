"""Eligibility domain events."""

from __future__ import annotations

from apps.core.events import DomainEvent


class _EligibilityEvent(DomainEvent):
    """Base event carrying common Eligibility identity."""

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        eligibility_id,
        patient_id,
        organization_id,
        **extra,
    ) -> None:
        """Initialize the event payload."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "eligibility_id": str(eligibility_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                **extra,
            },
        )


class EligibilityCreatedEvent(_EligibilityEvent):
    """Represent creation of an Eligibility request."""

    event_type = "revenue_cycle.eligibility.created"


class EligibilityUpdatedEvent(_EligibilityEvent):
    """Represent an Eligibility update."""

    event_type = "revenue_cycle.eligibility.updated"


class EligibilityDeletedEvent(_EligibilityEvent):
    """Represent deletion of an Eligibility request."""

    event_type = "revenue_cycle.eligibility.deleted"


class EligibilityRestoredEvent(_EligibilityEvent):
    """Represent restoration of an Eligibility request."""

    event_type = "revenue_cycle.eligibility.restored"


class EligibilityStatusChangedEvent(_EligibilityEvent):
    """Represent an Eligibility lifecycle transition."""

    event_type = "revenue_cycle.eligibility.status_changed"


__all__ = (
    "EligibilityCreatedEvent",
    "EligibilityDeletedEvent",
    "EligibilityRestoredEvent",
    "EligibilityStatusChangedEvent",
    "EligibilityUpdatedEvent",
)
