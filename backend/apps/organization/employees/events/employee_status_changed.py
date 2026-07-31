"""
Employee status changed domain event.
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
class EmployeeStatusChangedEvent(
    DomainEvent,
):
    """
    Fired when employee employment status changes.

    Used by:

    - Audit logging
    - Notifications
    - Search indexing
    - Analytics
    - External integrations
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    organization_id: UUID

    previous_status: str

    new_status: str


__all__ = ("EmployeeStatusChangedEvent",)
