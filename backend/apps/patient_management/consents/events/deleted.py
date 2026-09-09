"""
Patient Consent deleted domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class PatientConsentDeletedEvent(
    DomainEvent,
):
    """
    Emitted after a Patient Consent is deleted.
    """

    tenant_id: UUID
    actor_id: UUID
    consent_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("PatientConsentDeletedEvent",)
