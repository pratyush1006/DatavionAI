"""Organization-scoped Document RBAC adapters."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.engines import user_has_permission
from apps.platform.rbac.permissions.base import RBACPermissionBase


class _DocumentOrganizationPermission(RBACPermissionBase):
    """Require a Document permission within the active organization and tenant."""

    def has_permission(self, request: Any, view: Any) -> bool:
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        organization = getattr(view, "current_organization", None)
        tenant = getattr(view, "current_tenant", None)
        if organization is None or tenant is None:
            return False
        if getattr(organization, "tenant_id", None) != getattr(tenant, "id", None):
            return False
        return user_has_permission(
            user=user,
            permission=self.permission_code,
            organization=organization,
        )


class CanViewDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to view documents."
    permission_code = "documents.view"


class CanCreateDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to create documents."
    permission_code = "documents.create"


class CanUploadDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to upload documents."
    permission_code = "documents.upload"


class CanUpdateDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to update documents."
    permission_code = "documents.update"


class CanDeleteDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to delete documents."
    permission_code = "documents.delete"


class CanManageDocumentVersions(_DocumentOrganizationPermission):
    message = "You do not have permission to manage document versions."
    permission_code = "documents.version.manage"


class CanDownloadDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to download documents."
    permission_code = "documents.download"


class CanShareDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to share documents."
    permission_code = "documents.share"


class CanArchiveDocument(_DocumentOrganizationPermission):
    message = "You do not have permission to archive documents."
    permission_code = "documents.archive"


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
