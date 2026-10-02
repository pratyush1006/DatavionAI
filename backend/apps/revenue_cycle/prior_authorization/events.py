"""Prior Authorization domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class PriorAuthorizationEvent(DomainEvent):
    """Base event emitted for Prior Authorization changes."""

    verification_id: UUID
    organization_id: UUID
    patient_id: UUID
    status: str
    payload: dict[str, Any]


class PriorAuthorizationCreatedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is created."""


class PriorAuthorizationUpdatedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is updated."""


class PriorAuthorizationDeletedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is soft-deleted."""


class PriorAuthorizationRestoredEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization is restored."""


class PriorAuthorizationStatusChangedEvent(PriorAuthorizationEvent):
    """Emitted after an Prior Authorization lifecycle transition."""


__all__ = (
    "PriorAuthorizationCreatedEvent",
    "PriorAuthorizationDeletedEvent",
    "PriorAuthorizationEvent",
    "PriorAuthorizationRestoredEvent",
    "PriorAuthorizationStatusChangedEvent",
    "PriorAuthorizationUpdatedEvent",
)
