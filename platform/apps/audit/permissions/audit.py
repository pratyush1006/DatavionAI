"""
Audit permission classes.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewAudit(BasePermission):
    """
    Permission required to view audit logs.

    Currently any authenticated user is allowed.
    Replace this with RBAC permission checks when
    the audit permission service is implemented.
    """

    message = "You do not have permission to view audit logs."

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)
