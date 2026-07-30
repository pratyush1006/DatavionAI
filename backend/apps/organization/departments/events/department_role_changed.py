"""
Department role changed event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class DepartmentRoleChangedEvent(
    DomainEvent,
):
    department_id: UUID
    role_id: UUID


__all__ = ("DepartmentRoleChangedEvent",)
