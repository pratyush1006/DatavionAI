"""
Domain events emitted by Revenue Cycle Appeals.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class AppealCreated(DomainEvent):
    """Represent an appeal-created event."""

    appeal_id: UUID
    organization_id: UUID
    patient_id: UUID
    claim_reference: str


@dataclass(frozen=True, slots=True, kw_only=True)
class AppealTransitioned(DomainEvent):
    """Represent an appeal lifecycle transition event."""

    appeal_id: UUID
    organization_id: UUID
    from_status: str
    to_status: str


@dataclass(frozen=True, slots=True, kw_only=True)
class AppealDeleted(DomainEvent):
    """Represent an appeal deletion event."""

    appeal_id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class AppealRestored(DomainEvent):
    """Represent an appeal restoration event."""

    appeal_id: UUID
    organization_id: UUID


__all__ = (
    "AppealCreated",
    "AppealDeleted",
    "AppealRestored",
    "AppealTransitioned",
)
