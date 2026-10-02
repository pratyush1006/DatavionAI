"""
Organization module disabled domain event.
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
class ModuleDisabledEvent(DomainEvent):
    """
    Raised when a module is disabled for an organization.
    """

    organization_id: UUID

    module_code: str


__all__: tuple[str, ...] = ("ModuleDisabledEvent",)
