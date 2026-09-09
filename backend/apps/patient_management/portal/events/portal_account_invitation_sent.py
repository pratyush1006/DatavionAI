"""
Patient Portal invitation domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientPortalAccountInvitationSentEvent(DomainEvent):
    """Emitted after a portal invitation has been issued."""

    tenant_id: UUID
    actor_id: UUID
    account_id: UUID
    patient_id: UUID
    organization_id: UUID
    email: str


__all__ = ("PatientPortalAccountInvitationSentEvent",)
