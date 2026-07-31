"""
Document selectors.

Central export point.
"""

from .document import (
    get_document_access_entries,
    get_document_by_id,
    get_document_versions,
    get_documents,
)

__all__ = (
    "get_documents",
    "get_document_by_id",
    "get_document_versions",
    "get_document_access_entries",
)
