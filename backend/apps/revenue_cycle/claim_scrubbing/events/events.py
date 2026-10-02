"""
Domain events emitted by Claim Scrubbing.

Claim Scrubbing follows the canonical DatavionOS event contract:
- DomainEvent defines the event type.
- publish_after_commit() dispatches only after the surrounding
  database transaction has committed successfully.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.core.events import DomainEvent, publish_after_commit


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


def claim_scrub_created(
    *,
    scrub_id: str,
    organization_id: str,
) -> None:
    """
    Publish a claim-scrub-created event after the current
    database transaction commits successfully.
    """

    publish_after_commit(
        ClaimScrubCreated(
            scrub_id=scrub_id,
            organization_id=organization_id,
        )
    )


def claim_scrub_completed(
    *,
    scrub_id: str,
    organization_id: str,
    status: str,
) -> None:
    """
    Publish a claim-scrub-completed event after the current
    database transaction commits successfully.
    """

    publish_after_commit(
        ClaimScrubCompleted(
            scrub_id=scrub_id,
            organization_id=organization_id,
            status=status,
        )
    )


__all__ = (
    "ClaimScrubCreated",
    "ClaimScrubCompleted",
    "claim_scrub_created",
    "claim_scrub_completed",
)
