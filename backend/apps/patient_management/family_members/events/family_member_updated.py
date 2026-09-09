"""
Family Member updated domain event.
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
class FamilyMemberUpdatedEvent(
    DomainEvent,
):
    """
    Fired when a family member is updated.

    Carries the changed fields required for downstream
    audit, integration, and analytics processing.
    """

    tenant_id: UUID
    actor_id: UUID
    family_member_id: UUID
    patient_id: UUID
    organization_id: UUID
    changes: dict[str, Any]


__all__ = ("FamilyMemberUpdatedEvent",)
