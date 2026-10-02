"""
Organization role resolver.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.models.organization_role import (
    OrganizationRole,
)


def resolve_organization_roles(
    *,
    user: User,
    organization: Organization | None = None,
) -> QuerySet[OrganizationRole]:
    """
    Resolve active organization roles.
    """

    queryset = OrganizationRole.objects.filter(
        user=user,
        is_active=True,
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    return queryset.select_related(
        "role",
        "organization",
    )


__all__ = [
    "resolve_organization_roles",
]
