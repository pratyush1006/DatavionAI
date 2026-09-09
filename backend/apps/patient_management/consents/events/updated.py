"""
Patient Consent updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class PatientConsentUpdatedEvent(
    DomainEvent,
):
    """
    Emitted after a Patient Consent is updated.
    """

    tenant_id: UUID
    actor_id: UUID
    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    changes: dict[str, Any]


__all__ = ("PatientConsentUpdatedEvent",)
