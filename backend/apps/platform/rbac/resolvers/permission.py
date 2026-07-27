"""
Permission resolution helpers.

Resolves effective permissions from:

1. Platform roles
2. Organization roles
3. Role hierarchy
4. Role permissions
"""

from __future__ import annotations

from apps.platform.accounts.models import User
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.models import (
    Permission,
    Role,
)

from .hierarchy import (
    resolve_inherited_roles,
)
from .organization import (
    resolve_organization_roles,
)
from .role import (
    resolve_user_roles,
)


def resolve_permissions(
    *,
    user: User,
    organization: Organization | None = None,
) -> set[str]:
    """
       Resolve effective permission codes.

       Resolution:

       User
         |
         +----------------+
         |                |
         v                v
    Platform RBAC   Organization RBAC
         |                |
         +----------------+
                  |
                  v
           Role Hierarchy
                  |
                  v
           Role Permissions
                  |
                  v
           Permission Codes
    """

    #
    # Collect role IDs.
    #
    # Keep QuerySet compatibility for hierarchy resolver.
    #
    role_ids: set[str] = set(
        resolve_user_roles(
            user=user,
        ).values_list(
            "id",
            flat=True,
        )
    )

    #
    # Organization scoped roles.
    #
    if organization is not None:
        role_ids.update(
            resolve_organization_roles(
                user=user,
                organization=organization,
            ).values_list(
                "id",
                flat=True,
            )
        )

    if not role_ids:
        return set()

    #
    # Rebuild QuerySet.
    #
    # Required by hierarchy resolver.
    #
    roles = Role.objects.filter(
        id__in=role_ids,
    )

    #
    # Resolve inherited roles.
    #
    roles = resolve_inherited_roles(
        roles=roles,
    )

    if not roles.exists():
        return set()

    #
    # Resolve permissions.
    #
    permissions = (
        Permission.objects.active()
        .filter(
            role_permissions__role__in=roles,
            role_permissions__is_active=True,
        )
        .distinct()
        .values_list(
            "code",
            flat=True,
        )
    )

    return set(
        permissions,
    )


__all__ = [
    "resolve_permissions",
]
