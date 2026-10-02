"""
Patient Registration completed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationCompletedEvent(DomainEvent):
    """
    Published after a patient registration is successfully completed.

    The event contains only identifiers and completion metadata.
    Sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    completed_at: str | None
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.completed"


__all__ = ("RegistrationCompletedEvent",)
