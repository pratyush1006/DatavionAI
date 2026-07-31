"""
Document services.

Central export point.
"""

from .document import (
    archive_document,
    create_document,
    delete_document,
    update_document,
)
from .version import (
    create_document_version,
)

__all__ = (
    "create_document",
    "update_document",
    "archive_document",
    "delete_document",
    "create_document_version",
)
