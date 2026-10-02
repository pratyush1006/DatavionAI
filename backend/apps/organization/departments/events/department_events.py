"""
Department domain events.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events.base import DomainEvent


@dataclass(frozen=True, slots=True)
class DepartmentCreatedEvent(DomainEvent):
    department_id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class DepartmentUpdatedEvent(DomainEvent):
    department_id: UUID
    organization_id: UUID
    changed_fields: list[str]


@dataclass(frozen=True, slots=True)
class DepartmentActivatedEvent(DomainEvent):
    department_id: UUID


@dataclass(frozen=True, slots=True)
class DepartmentDeactivatedEvent(DomainEvent):
    department_id: UUID


@dataclass(frozen=True, slots=True)
class DepartmentSuspendedEvent(DomainEvent):
    department_id: UUID


@dataclass(frozen=True, slots=True)
class DepartmentRestoredEvent(DomainEvent):
    department_id: UUID


@dataclass(frozen=True, slots=True)
class DepartmentDeletedEvent(DomainEvent):
    department_id: UUID


__all__ = (
    "DepartmentCreatedEvent",
    "DepartmentUpdatedEvent",
    "DepartmentActivatedEvent",
    "DepartmentDeactivatedEvent",
    "DepartmentSuspendedEvent",
    "DepartmentRestoredEvent",
    "DepartmentDeletedEvent",
)
