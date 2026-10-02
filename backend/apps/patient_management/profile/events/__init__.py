"""
Patient Profile domain events.
"""

from .profile_created import (
    ProfileCreatedEvent,
)
from .profile_deleted import (
    ProfileDeletedEvent,
)
from .profile_updated import (
    ProfileUpdatedEvent,
)

__all__ = (
    "ProfileCreatedEvent",
    "ProfileDeletedEvent",
    "ProfileUpdatedEvent",
)
