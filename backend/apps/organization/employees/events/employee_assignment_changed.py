"""
Employee assignment changed domain event.
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
class EmployeeAssignmentChangedEvent(
    DomainEvent,
):
    """
    Fired when an employee assignment changes.

    Carries enough context for:

    - Audit logging
    - Notifications
    - Workflow tracking
    - Organization synchronization
    - Analytics pipelines
    - Integration events
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    organization_id: UUID

    previous_department_id: UUID | None

    new_department_id: UUID | None

    previous_team_id: UUID | None

    new_team_id: UUID | None

    previous_supervisor_id: UUID | None

    new_supervisor_id: UUID | None


__all__ = ("EmployeeAssignmentChangedEvent",)
