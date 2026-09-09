"""Domain events emitted by claim scrubbing."""

from __future__ import annotations

from dataclasses import dataclass

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class ClaimScrubCreated(DomainEvent):
    """Signal that a claim scrub was created."""

    scrub_id: str
    organization_id: str


@dataclass(frozen=True)
class ClaimScrubCompleted(DomainEvent):
    """Signal that a claim scrub completed."""

    scrub_id: str
    organization_id: str
    status: str


def claim_scrub_created(*, scrub_id: str, organization_id: str) -> None:
    """Publish a scrub-created event through the project event bus."""

    DomainEvent.publish(
        ClaimScrubCreated(scrub_id=scrub_id, organization_id=organization_id)
    )


def claim_scrub_completed(*, scrub_id: str, organization_id: str, status: str) -> None:
    """Publish a scrub-completed event through the project event bus."""

    DomainEvent.publish(
        ClaimScrubCompleted(
            scrub_id=scrub_id, organization_id=organization_id, status=status
        )
    )


__all__ = (
    "ClaimScrubCreated",
    "ClaimScrubCompleted",
    "claim_scrub_created",
    "claim_scrub_completed",
)
