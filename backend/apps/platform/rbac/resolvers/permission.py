"""
Permission resolution helpers.
"""

from __future__ import annotations

from apps.platform.accounts.models import User
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.models import (
    Permission,
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
    Resolve the effective permission codes for a user.

    Resolution order:

    1. Direct user roles
    2. Organization roles
    3. Role hierarchy inheritance
    4. Role permissions
    """

    #
    # Direct user roles.
    #
    roles = resolve_user_roles(
        user=user,
    )

    #
    # Organization-specific roles.
    #
    if organization is not None:
        roles = roles.union(
            resolve_organization_roles(
                user=user,
                organization=organization,
            ),
        )

    #
    # Expand inherited roles.
    #
    roles = resolve_inherited_roles(
        roles=roles,
    )

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
    )

    return set(
        permissions.values_list(
            "code",
            flat=True,
        ),
    )


__all__ = [
    "resolve_permissions",
]
