"""Insurance Verification domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class InsuranceVerificationEvent(DomainEvent):
    """Base event emitted for Insurance Verification changes."""

    verification_id: UUID
    organization_id: UUID
    patient_id: UUID
    status: str
    payload: dict[str, Any]


class InsuranceVerificationCreatedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is created."""


class InsuranceVerificationUpdatedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is updated."""


class InsuranceVerificationDeletedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is soft-deleted."""


class InsuranceVerificationRestoredEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification is restored."""


class InsuranceVerificationStatusChangedEvent(InsuranceVerificationEvent):
    """Emitted after an Insurance Verification lifecycle transition."""


__all__ = (
    "InsuranceVerificationCreatedEvent",
    "InsuranceVerificationDeletedEvent",
    "InsuranceVerificationEvent",
    "InsuranceVerificationRestoredEvent",
    "InsuranceVerificationStatusChangedEvent",
    "InsuranceVerificationUpdatedEvent",
)
