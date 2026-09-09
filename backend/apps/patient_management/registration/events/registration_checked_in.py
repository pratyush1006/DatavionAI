"""
Patient Registration checked-in domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationCheckedInEvent(DomainEvent):
    """
    Published after a patient registration is successfully checked in.

    The event contains only identifiers and registration state metadata.
    Sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    checked_in_at: str | None
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.checked_in"


__all__ = ("RegistrationCheckedInEvent",)
