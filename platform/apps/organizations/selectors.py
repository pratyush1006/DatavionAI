"""
Read-only selectors for the Organizations app.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.organizations.models import Organization

type OrganizationQuerySet = QuerySet[Organization]

ORGANIZATION_LIST_FIELDS = (
    "id",
    "name",
    "code",
    "organization_type",
    "city",
    "country",
    "is_active",
)


def get_organizations(
    *,
    include_inactive: bool = False,
) -> OrganizationQuerySet:
    """
    Return organizations ordered by name.

    By default, only active organizations are returned.
    """

    queryset = Organization.objects.only(
        *ORGANIZATION_LIST_FIELDS,
    ).order_by(
        "name",
    )

    if not include_inactive:
        queryset = queryset.active()

    return queryset


def get_organization_by_id(
    organization_id: int,
) -> Organization:
    """
    Return a single organization by its primary key.
    """

    return get_object_or_404(
        get_organizations(
            include_inactive=True,
        ),
        pk=organization_id,
    )
