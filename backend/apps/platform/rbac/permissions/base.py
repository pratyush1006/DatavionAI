"""
RBAC base permission classes.

Central authorization layer for DatavionOS RBAC.

Responsibilities:

- Validate authenticated users
- Resolve organization context
- Delegate authorization to RBAC engine
- Support multi-tenant permissions
- Keep API permissions centralized
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import (
    Request,
)
from rest_framework.views import (
    APIView,
)

from apps.platform.rbac.engines import (
    user_has_permission,
)


class RBACPermissionBase(
    BasePermission,
):
    """
    Base RBAC permission checker.

    All RBAC API permissions inherit
    from this class.

    Authorization flow:

    Request
        |
        v
    Authenticated User
        |
        v
    Organization Context
        |
        v
    RBAC Engine
        |
        v
    Effective Permissions
    """

    permission_code: str = ""

    message = "You do not have permission to perform this action."

    def _get_organization(
        self,
        request: Request,
    ):
        """
        Resolve organization context.

        Priority:

        1. Tenant middleware context
        2. Request organization context
        3. X-Organization-ID header

        Header fallback supports:
        - API clients
        - Automated tests
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        if organization:
            return organization

        organization_id = request.headers.get(
            "X-Organization-ID",
        )

        if not organization_id:
            return None

        from apps.platform.organizations.models import (
            Organization,
        )

        return Organization.objects.filter(
            id=organization_id,
        ).first()

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Validate RBAC permission.
        """

        user = getattr(
            request,
            "user",
            None,
        )

        if not user or not user.is_authenticated:
            return False

        if not self.permission_code:
            return False

        organization = self._get_organization(
            request,
        )

        return user_has_permission(
            user=user,
            permission=self.permission_code,
            organization=organization,
        )


__all__ = [
    "RBACPermissionBase",
]
