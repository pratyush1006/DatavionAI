"""
Organization hierarchy changed domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class HierarchyChangedEvent(DomainEvent):
    """
    Raised when the organization hierarchy changes.
    """

    organization_id: UUID

    parent_organization_id: UUID | None

    relationship_type: str


__all__: tuple[str, ...] = ("HierarchyChangedEvent",)
