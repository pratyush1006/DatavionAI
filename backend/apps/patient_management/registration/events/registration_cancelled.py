"""
Patient Registration cancelled domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationCancelledEvent(DomainEvent):
    """
    Published after a patient registration is successfully cancelled.

    The event contains identifiers and structured cancellation metadata.
    Free-form cancellation notes are intentionally excluded to reduce
    unnecessary sensitive-data propagation through the event system.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    cancellation_reason: str
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.cancelled"


__all__ = ("RegistrationCancelledEvent",)
