"""
Document RBAC permissions.

Document bounded context permission adapters.

Uses the DatavionOS centralized RBAC engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewDocument(
    RBACPermissionBase,
):
    """
    Allows viewing documents.
    """

    message = "You do not have permission to view documents."

    permission_code = "documents.view"


class CanCreateDocument(
    RBACPermissionBase,
):
    """
    Allows creating documents.
    """

    message = "You do not have permission to create documents."

    permission_code = "documents.create"


class CanUpdateDocument(
    RBACPermissionBase,
):
    """
    Allows updating documents.
    """

    message = "You do not have permission to update documents."

    permission_code = "documents.update"


class CanDeleteDocument(
    RBACPermissionBase,
):
    """
    Allows deleting documents.
    """

    message = "You do not have permission to delete documents."

    permission_code = "documents.delete"


class CanManageDocumentVersions(
    RBACPermissionBase,
):
    """
    Allows managing document versions.
    """

    message = "You do not have permission to manage document versions."

    permission_code = "documents.version.manage"


class CanDownloadDocument(
    RBACPermissionBase,
):
    """
    Allows downloading documents.
    """

    message = "You do not have permission to download documents."

    permission_code = "documents.download"


class CanShareDocument(
    RBACPermissionBase,
):
    """
    Allows sharing documents.
    """

    message = "You do not have permission to share documents."

    permission_code = "documents.share"


class CanArchiveDocument(
    RBACPermissionBase,
):
    """
    Allows archiving documents.
    """

    message = "You do not have permission to archive documents."

    permission_code = "documents.archive"


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
