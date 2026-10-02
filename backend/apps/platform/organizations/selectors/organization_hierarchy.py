"""
Read-only selectors for organization hierarchies.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationHierarchyQuerySet = QuerySet[OrganizationHierarchy]


def _organization_pk(
    organization: Organization | Any,
) -> Any:
    """
    Return an organization primary key.
    """

    return getattr(
        organization,
        "pk",
        organization,
    )


def get_organization_hierarchy_by_id(
    hierarchy_id: Any,
) -> OrganizationHierarchy:
    """
    Return an organization hierarchy by primary key.
    """

    return get_object_or_404(
        OrganizationHierarchy.objects.with_related(),
        pk=hierarchy_id,
    )


def get_organization_hierarchies(
    *,
    parent_organization: Organization | Any | None = None,
    child_organization: Organization | Any | None = None,
    relationship_type: str | None = None,
    status: str | None = None,
) -> OrganizationHierarchyQuerySet:
    """
    Return organization hierarchy relationships.
    """

    queryset = OrganizationHierarchy.objects.with_related()

    if parent_organization is not None:
        queryset = queryset.by_parent(
            _organization_pk(parent_organization),
        )

    if child_organization is not None:
        queryset = queryset.by_child(
            _organization_pk(child_organization),
        )

    if relationship_type is not None:
        queryset = queryset.by_relationship_type(
            relationship_type,
        )

    if status is not None:
        queryset = queryset.by_status(
            status,
        )

    return queryset


def get_child_hierarchies(
    *,
    parent_organization: Organization | Any,
) -> OrganizationHierarchyQuerySet:
    """
    Return child hierarchy relationships.
    """

    return OrganizationHierarchy.objects.with_related().by_parent(
        _organization_pk(parent_organization),
    )


def get_parent_hierarchies(
    *,
    child_organization: Organization | Any,
) -> OrganizationHierarchyQuerySet:
    """
    Return parent hierarchy relationships.
    """

    return OrganizationHierarchy.objects.with_related().by_child(
        _organization_pk(child_organization),
    )


def search_organization_hierarchies(
    *,
    query: str,
) -> OrganizationHierarchyQuerySet:
    """
    Search organization hierarchy relationships.
    """

    return OrganizationHierarchy.objects.with_related().search(
        query.strip(),
    )


__all__: tuple[str, ...] = (
    "OrganizationHierarchyQuerySet",
    "get_child_hierarchies",
    "get_organization_hierarchies",
    "get_organization_hierarchy_by_id",
    "get_parent_hierarchies",
    "search_organization_hierarchies",
)
