"""
Department member assigned event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class DepartmentMemberAssignedEvent(
    DomainEvent,
):
    department_id: UUID
    employee_id: UUID


__all__ = ("DepartmentMemberAssignedEvent",)
