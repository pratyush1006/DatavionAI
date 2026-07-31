"""
Employee updated domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import (
    DomainEvent,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EmployeeUpdatedEvent(
    DomainEvent,
):
    """
    Fired when an employee is updated.

    Carries enough context for:

    - Audit logging
    - Notifications
    - Search indexing
    - Integration events
    - Analytics pipelines
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    organization_id: UUID


__all__ = ("EmployeeUpdatedEvent",)
