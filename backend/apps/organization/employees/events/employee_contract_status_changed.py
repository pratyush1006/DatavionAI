"""
Employee contract status changed domain event.
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
class EmployeeContractStatusChangedEvent(
    DomainEvent,
):
    """
    Fired when employee contract status changes.

    Used for:

    - Audit logging
    - Notifications
    - HR workflows
    - Compliance tracking
    - Analytics
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    contract_id: UUID

    organization_id: UUID

    previous_status: str

    new_status: str


__all__ = ("EmployeeContractStatusChangedEvent",)
