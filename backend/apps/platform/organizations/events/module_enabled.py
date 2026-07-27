"""
Organization module enabled domain event.
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
class ModuleEnabledEvent(DomainEvent):
    """
    Raised when a module is enabled for an organization.
    """

    organization_id: UUID

    module_code: str


__all__: tuple[str, ...] = ("ModuleEnabledEvent",)
