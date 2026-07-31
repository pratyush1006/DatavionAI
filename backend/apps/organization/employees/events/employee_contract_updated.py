"""
Employee contract updated domain event.
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
class EmployeeContractUpdatedEvent(
    DomainEvent,
):
    """
    Fired when an employee contract changes.
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    contract_id: UUID

    organization_id: UUID


__all__ = ("EmployeeContractUpdatedEvent",)
