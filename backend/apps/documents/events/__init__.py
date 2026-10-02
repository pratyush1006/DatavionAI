"""
Document domain events.

Central export point.
"""

from .document_created import (
    DocumentCreatedEvent,
)
from .document_deleted import (
    DocumentDeletedEvent,
)
from .document_updated import (
    DocumentUpdatedEvent,
)
from .document_version_created import (
    DocumentVersionCreatedEvent,
)

__all__ = (
    "DocumentCreatedEvent",
    "DocumentUpdatedEvent",
    "DocumentDeletedEvent",
    "DocumentVersionCreatedEvent",
)
