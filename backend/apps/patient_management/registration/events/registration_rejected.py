"""
Patient Registration rejected domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationRejectedEvent(DomainEvent):
    """
    Published after a patient registration is successfully rejected.

    The event contains only identifiers and registration state metadata.
    Sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.rejected"


__all__ = ("RegistrationRejectedEvent",)
