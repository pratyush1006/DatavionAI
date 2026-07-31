"""
Document RBAC permissions.

Central export point.
"""

from .document import (
    CanArchiveDocument,
    CanCreateDocument,
    CanDeleteDocument,
    CanDownloadDocument,
    CanManageDocumentVersions,
    CanShareDocument,
    CanUpdateDocument,
    CanViewDocument,
)

__all__ = (
    "CanViewDocument",
    "CanCreateDocument",
    "CanUpdateDocument",
    "CanDeleteDocument",
    "CanManageDocumentVersions",
    "CanDownloadDocument",
    "CanShareDocument",
    "CanArchiveDocument",
)
