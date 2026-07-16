"""
RBAC authorization engine.
"""

from __future__ import annotations

from apps.platform.accounts.models import (
    User,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.resolvers import (
    resolve_permissions,
)


def get_effective_permissions(
    *,
    user: User,
    organization: Organization | None = None,
) -> set[str]:
    """
    Return the effective permission codes for a user.

    This is the single entry point for permission resolution.
    """

    if not user.is_authenticated:
        return set()

    return resolve_permissions(
        user=user,
        organization=organization,
    )


def user_has_permission(
    *,
    user: User,
    permission: str,
    organization: Organization | None = None,
) -> bool:
    """
    Determine whether the user has the requested permission.
    """

    return permission in get_effective_permissions(
        user=user,
        organization=organization,
    )


__all__ = [
    "get_effective_permissions",
    "user_has_permission",
]
