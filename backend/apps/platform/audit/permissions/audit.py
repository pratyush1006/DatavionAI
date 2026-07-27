"""
Audit permission classes.

Uses DatavionOS RBAC authorization engine.
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)

from apps.platform.rbac.engines import (
    user_has_permission,
)


class AuditBasePermission(
    BasePermission,
):
    """
    Base permission for Audit module.

    Delegates authorization to
    DatavionOS RBAC engine.
    """

    permission_code: str = ""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Validate audit permission.
        """

        user = getattr(
            request,
            "user",
            None,
        )

        if not user or not user.is_authenticated:
            return False

        return user_has_permission(
            user=user,
            permission=self.permission_code,
        )


class CanViewAudit(
    AuditBasePermission,
):
    """
    Permission required to view audit logs.
    """

    message = "You do not have permission to view audit logs."

    permission_code = "audit.view"


class CanExportAudit(
    AuditBasePermission,
):
    """
    Permission required to export audit logs.
    """

    message = "You do not have permission to export audit logs."

    permission_code = "audit.export"


__all__ = [
    "AuditBasePermission",
    "CanViewAudit",
    "CanExportAudit",
]
