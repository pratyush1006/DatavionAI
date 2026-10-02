"""Domain events for payment posting."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class PaymentPostingCreatedEvent(DomainEvent):
    """Signal that a payment posting was created."""

    posting_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True)
class PaymentPostingUpdatedEvent(DomainEvent):
    """Signal that a payment posting was updated."""

    posting_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class PaymentPostedEvent(DomainEvent):
    """Signal that a payment posting became posted."""

    posting_id: UUID
    organization_id: UUID
    amount: str


@dataclass(frozen=True)
class PaymentPostingReversedEvent(DomainEvent):
    """Signal that a payment posting was reversed."""

    posting_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class PaymentPostingDeletedEvent(DomainEvent):
    """Signal that a payment posting was soft-deleted."""

    posting_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class PaymentPostingRestoredEvent(DomainEvent):
    """Signal that a payment posting was restored."""

    posting_id: UUID
    organization_id: UUID


__all__ = (
    "PaymentPostedEvent",
    "PaymentPostingCreatedEvent",
    "PaymentPostingDeletedEvent",
    "PaymentPostingReversedEvent",
    "PaymentPostingRestoredEvent",
    "PaymentPostingUpdatedEvent",
)
