"""
Read-only selectors for the Organizations application.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization

type OrganizationQuerySet = QuerySet[Organization]


ORGANIZATION_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "display_name",
    "slug",
    "code",
    "category",
    "organization_type",
    "status",
    "city",
    "state",
    "country",
    "is_active",
)


def get_organizations(
    *,
    include_inactive: bool = False,
) -> OrganizationQuerySet:
    """
    Return organizations.
    """

    queryset = Organization.objects.only(
        *ORGANIZATION_LIST_FIELDS,
    )

    if not include_inactive:
        queryset = queryset.active()

    return queryset


def get_organization_by_id(
    organization_id: int,
) -> Organization:
    """
    Return an organization by its primary key.
    """

    return get_object_or_404(
        get_organizations(
            include_inactive=True,
        ),
        pk=organization_id,
    )


def get_organization_by_code(
    code: str,
) -> Organization:
    """
    Return an organization by its unique code.
    """

    return get_object_or_404(
        get_organizations(
            include_inactive=True,
        ),
        code=code,
    )


def get_organization_by_slug(
    slug: str,
) -> Organization:
    """
    Return an organization by its unique slug.
    """

    return get_object_or_404(
        get_organizations(
            include_inactive=True,
        ),
        slug=slug,
    )


def organization_exists(
    *,
    code: str,
    include_inactive: bool = True,
) -> bool:
    """
    Return whether an organization exists.
    """

    return (
        get_organizations(
            include_inactive=include_inactive,
        )
        .filter(
            code=code,
        )
        .exists()
    )


__all__ = [
    "OrganizationQuerySet",
    "get_organization_by_code",
    "get_organization_by_id",
    "get_organization_by_slug",
    "get_organizations",
    "organization_exists",
]
