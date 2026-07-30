"""
Permission resolver.

DatavionOS permission bridge.

Connects the DatavionOS kernel
with the platform RBAC engine.

Resolution hierarchy:

1. Platform RBAC
   User
    |
   UserRole
    |
   Role
    |
   Permissions


2. Organization RBAC
   Organization
    |
   OrganizationRole
    |
   User
    |
   Role
    |
   Permissions


3. Effective Permission Set
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.resolvers.permission import (
    resolve_permissions,
)

User = get_user_model()


class PermissionResolver:
    """
    Resolve effective DatavionOS permissions.
    """

    def resolve(
        self,
        *,
        user: User,
        organization: Organization | None = None,
    ) -> set[str]:
        """
        Return effective permissions.

        Combines:

        - Global platform permissions
        - Organization scoped permissions
        """

        if not user.is_authenticated:
            return set()

        permissions = resolve_permissions(
            user=user,
            organization=organization,
        )

        return set(
            permissions,
        )

    def has_permission(
        self,
        *,
        user: User,
        permission: str,
        organization: Organization | None = None,
    ) -> bool:
        """
        Check single permission.
        """

        return permission in self.resolve(
            user=user,
            organization=organization,
        )

    def has_any_permission(
        self,
        *,
        user: User,
        permissions: set[str],
        organization: Organization | None = None,
    ) -> bool:
        """
        Check whether user has any permission.
        """

        user_permissions = self.resolve(
            user=user,
            organization=organization,
        )

        return bool(
            user_permissions.intersection(
                permissions,
            )
        )

    def has_all_permissions(
        self,
        *,
        user: User,
        permissions: set[str],
        organization: Organization | None = None,
    ) -> bool:
        """
        Check whether user has all permissions.
        """

        user_permissions = self.resolve(
            user=user,
            organization=organization,
        )

        return permissions.issubset(
            user_permissions,
        )


permission_resolver = PermissionResolver()


__all__ = [
    "PermissionResolver",
    "permission_resolver",
]
