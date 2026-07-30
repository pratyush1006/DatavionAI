"""
Department settings updated event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class DepartmentSettingsUpdatedEvent(
    DomainEvent,
):
    department_id: UUID


__all__ = ("DepartmentSettingsUpdatedEvent",)
