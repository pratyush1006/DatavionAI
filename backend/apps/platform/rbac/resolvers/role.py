"""
Role resolution helpers.

Resolves tenant-aware RBAC roles for DatavionOS.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.platform.accounts.models import User
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.tenancy.models import (
    Tenant,
)


def resolve_user_roles(
    *,
    user: User,
    tenant: Tenant | None = None,
) -> QuerySet[Role]:
    """
    Resolve active roles assigned to a user.

    Resolution scope:

    - User
    - Tenant membership
    - Active role assignment

    Inherited roles are handled separately
    by hierarchy resolver.
    """

    queryset = Role.objects.active().filter(
        user_roles__user=user,
        user_roles__is_active=True,
        user_roles__is_deleted=False,
    )

    if tenant is not None:
        queryset = queryset.filter(
            user_roles__tenant=tenant,
        )

    return queryset.distinct()


__all__ = [
    "resolve_user_roles",
]
