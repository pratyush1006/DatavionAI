"""
Employee contract created domain event.
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
class EmployeeContractCreatedEvent(
    DomainEvent,
):
    """
    Fired when an employee contract is created.

    Carries enough context for:

    - Audit logging
    - Notifications
    - Workflow tracking
    - Analytics pipelines
    - Integration events
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    contract_id: UUID

    organization_id: UUID


__all__ = ("EmployeeContractCreatedEvent",)
