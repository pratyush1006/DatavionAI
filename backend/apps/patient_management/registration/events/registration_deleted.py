"""
Patient Registration deleted domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationDeletedEvent(DomainEvent):
    """
    Published after a patient registration is successfully deleted.

    The event contains only identifiers and immutable registration metadata.
    Sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.deleted"


__all__ = ("RegistrationDeletedEvent",)
