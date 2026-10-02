"""Domain events emitted by ERA workflows."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class ERAEvent(DomainEvent):
    """Represent an ERA domain event."""

    era_id: UUID
    organization_id: UUID
    action: str


__all__ = ("ERAEvent",)
