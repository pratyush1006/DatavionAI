"""
Team created domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(
    frozen=True,
    slots=True,
)
class TeamCreatedEvent:
    """
    Published when a team is created.
    """

    tenant_id: UUID

    actor_id: UUID

    team_id: UUID

    organization_id: UUID

    event_id: UUID = uuid4()


__all__ = ("TeamCreatedEvent",)
