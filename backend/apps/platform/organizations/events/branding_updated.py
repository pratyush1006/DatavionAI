"""
Organization branding updated domain event.
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
class BrandingUpdatedEvent(DomainEvent):
    """
    Raised when organization branding is updated.
    """

    organization_id: UUID

    changed_fields: tuple[str, ...]


__all__: tuple[str, ...] = ("BrandingUpdatedEvent",)
