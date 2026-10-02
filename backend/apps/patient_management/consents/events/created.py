"""
Patient Consent created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class PatientConsentCreatedEvent(
    DomainEvent,
):
    """
    Emitted after a Patient Consent is successfully created.
    """

    tenant_id: UUID
    actor_id: UUID
    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    purpose: str
    status: str


__all__ = ("PatientConsentCreatedEvent",)
