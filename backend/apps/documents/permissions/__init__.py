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
    CanUploadDocument,
    CanViewDocument,
)

__all__ = (
    "CanViewDocument",
    "CanCreateDocument",
    "CanUploadDocument",
    "CanUpdateDocument",
    "CanDeleteDocument",
    "CanManageDocumentVersions",
    "CanDownloadDocument",
    "CanShareDocument",
    "CanArchiveDocument",
)
