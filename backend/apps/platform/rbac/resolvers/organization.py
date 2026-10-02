"""
Organization role resolution helpers.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.platform.accounts.models import User
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.models import (
    Role,
)


def resolve_organization_roles(
    *,
    user: User,
    organization: Organization,
) -> QuerySet[Role]:
    """
    Resolve all active roles assigned to a user
    within an organization.
    """

    return (
        Role.objects.active()
        .filter(
            organization_roles__organization=organization,
            organization_roles__user=user,
            organization_roles__is_active=True,
        )
        .distinct()
    )


__all__ = [
    "resolve_organization_roles",
]
