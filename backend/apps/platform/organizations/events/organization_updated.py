"""
Organization updated domain event.
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
class OrganizationUpdatedEvent(DomainEvent):
    """
    Raised after organization information is updated.
    """

    organization_id: UUID

    changed_fields: tuple[str, ...]


__all__: tuple[str, ...] = ("OrganizationUpdatedEvent",)
