"""
Patient Registration verified domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class RegistrationVerifiedEvent(DomainEvent):
    """
    Published after a patient registration is successfully verified.

    The event contains only identifiers and verification metadata.
    Sensitive patient information is intentionally excluded.
    """

    tenant_id: UUID
    actor_id: UUID
    registration_id: UUID
    patient_id: UUID
    organization_id: UUID
    registration_number: str
    verification_method: str | None
    verified_at: str | None
    registration_status: str

    @property
    def event_type(self) -> str:
        """Return the stable event type identifier."""
        return "patient_registration.verified"


__all__ = ("RegistrationVerifiedEvent",)
