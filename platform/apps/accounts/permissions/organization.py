"""
Organization permissions.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsOrganizationAdmin(BasePermission):
    """
    Allows access only to organization admins.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_staff


__all__ = [
    "IsOrganizationAdmin",
]
