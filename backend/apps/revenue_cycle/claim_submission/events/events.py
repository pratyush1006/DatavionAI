"""Domain events emitted by claim submission workflows."""

from __future__ import annotations

from dataclasses import dataclass

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class ClaimSubmissionCreated(DomainEvent):
    """Signal creation of a claim submission."""

    submission_id: str
    organization_id: str


@dataclass(frozen=True)
class ClaimSubmissionUpdated(DomainEvent):
    """Signal update of a claim submission."""

    submission_id: str
    organization_id: str
    changes: dict


@dataclass(frozen=True)
class ClaimSubmissionStatusChanged(DomainEvent):
    """Signal a submission lifecycle transition."""

    submission_id: str
    organization_id: str
    previous_status: str
    status: str


@dataclass(frozen=True)
class ClaimSubmissionDeleted(DomainEvent):
    """Signal soft deletion of a submission."""

    submission_id: str
    organization_id: str


@dataclass(frozen=True)
class ClaimSubmissionRestored(DomainEvent):
    """Signal restoration of a submission."""

    submission_id: str
    organization_id: str


__all__ = (
    "ClaimSubmissionCreated",
    "ClaimSubmissionUpdated",
    "ClaimSubmissionStatusChanged",
    "ClaimSubmissionDeleted",
    "ClaimSubmissionRestored",
)
