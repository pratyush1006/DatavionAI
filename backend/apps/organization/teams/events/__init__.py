"""
Team domain events.
"""

from .team_created import (
    TeamCreatedEvent,
)
from .team_deleted import (
    TeamDeletedEvent,
)
from .team_updated import (
    TeamUpdatedEvent,
)

__all__ = (
    "TeamCreatedEvent",
    "TeamUpdatedEvent",
    "TeamDeletedEvent",
)
