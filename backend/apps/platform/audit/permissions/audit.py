"""
Audit permission classes.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewAudit(
    BasePermission,
):
    """
    Permission required to view audit logs.

    This is a temporary implementation. Once the
    RBAC module exposes a centralized permission
    service, this class should delegate permission
    evaluation to it.
    """

    message = "You do not have permission to view audit logs."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Determine whether the request is permitted.
        """

        user = getattr(
            request,
            "user",
            None,
        )

        #
        # TODO:
        # Replace with RBAC permission check.
        #
        # Example:
        #
        # return PermissionService.has_permission(
        #     user=user,
        #     permission="audit.view",
        # )
        #

        return bool(user and user.is_authenticated)


class CanExportAudit(
    BasePermission,
):
    """
    Permission required to export audit logs.

    Reserved for future RBAC integration.
    """

    message = "You do not have permission to export audit logs."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Determine whether export is permitted.
        """

        user = getattr(
            request,
            "user",
            None,
        )

        #
        # TODO:
        # Replace with RBAC permission check.
        #

        return bool(user and user.is_authenticated)


__all__ = [
    "CanViewAudit",
    "CanExportAudit",
]
