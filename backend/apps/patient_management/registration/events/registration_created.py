"""
Patient Registration created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class RegistrationCreatedEvent(DomainEvent):
    """
    Fired when a patient registration is created.

    The event contains registration metadata only. Clinical or otherwise
    sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    registration_type: str
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.created"


__all__ = ("RegistrationCreatedEvent",)
