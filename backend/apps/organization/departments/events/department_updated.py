"""
Department updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class DepartmentUpdatedEvent(
    DomainEvent,
):
    department_id: UUID
    organization_id: UUID


__all__ = ("DepartmentUpdatedEvent",)
