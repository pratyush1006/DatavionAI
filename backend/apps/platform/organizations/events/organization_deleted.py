"""
Organization deleted domain event.
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
class OrganizationDeletedEvent(DomainEvent):
    """
    Raised after an organization has been deleted.
    """

    organization_id: UUID

    hard_delete: bool = False


__all__: tuple[str, ...] = ("OrganizationDeletedEvent",)
