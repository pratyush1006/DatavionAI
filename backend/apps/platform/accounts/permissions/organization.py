"""
Organization permissions.
"""

from __future__ import annotations

from apps.platform.accounts.permissions.user import (
    IsAuthenticatedUser,
)


class IsOrganizationAdmin(IsAuthenticatedUser):
    """
    Permission requiring organization administrator access.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return (
            super().has_permission(
                request,
                view,
            )
            and request.user.is_staff
        )


__all__ = [
    "IsOrganizationAdmin",
]
