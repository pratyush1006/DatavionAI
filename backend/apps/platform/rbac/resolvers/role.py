"""
Role resolution helpers.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.platform.accounts.models import User
from apps.platform.rbac.models import (
    Role,
)


def resolve_user_roles(
    *,
    user: User,
) -> QuerySet[Role]:
    """
    Resolve all active roles directly assigned to a user.

    This resolver only returns direct role assignments.
    Inherited roles are resolved separately by the
    hierarchy resolver.
    """

    return (
        Role.objects.active()
        .filter(
            user_roles__user=user,
            user_roles__is_active=True,
            user_roles__is_deleted=False,
        )
        .distinct()
    )


__all__ = [
    "resolve_user_roles",
]
