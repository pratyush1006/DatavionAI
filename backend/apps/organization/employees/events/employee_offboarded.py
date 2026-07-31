"""
Employee offboarded domain event.
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
class EmployeeOffboardedEvent(
    DomainEvent,
):
    """
    Fired after employee offboarding completes.
    """

    tenant_id: UUID

    actor_id: UUID

    employee_id: UUID

    organization_id: UUID


__all__ = ("EmployeeOffboardedEvent",)
