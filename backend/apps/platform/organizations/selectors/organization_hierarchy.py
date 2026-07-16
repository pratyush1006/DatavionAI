"""
Selectors for OrganizationHierarchy.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationHierarchy,
)


def get_organization_hierarchy_by_id(
    hierarchy_id,
) -> OrganizationHierarchy:
    """
    Return an organization hierarchy by its identifier.
    """

    return get_object_or_404(
        OrganizationHierarchy.objects.with_related(),
        id=hierarchy_id,
    )


def get_organization_hierarchies(
    *,
    parent_organization=None,
    child_organization=None,
    relationship_type=None,
    status=None,
) -> QuerySet[OrganizationHierarchy]:
    """
    Return organization hierarchies with optional filters.
    """

    queryset = OrganizationHierarchy.objects.with_related()

    if parent_organization is not None:
        queryset = queryset.by_parent(
            (
                parent_organization.id
                if hasattr(parent_organization, "id")
                else parent_organization
            ),
        )

    if child_organization is not None:
        queryset = queryset.by_child(
            (
                child_organization.id
                if hasattr(child_organization, "id")
                else child_organization
            ),
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
    parent_organization_id,
) -> QuerySet[OrganizationHierarchy]:
    """
    Return all child hierarchy relationships.
    """

    return OrganizationHierarchy.objects.with_related().by_parent(
        parent_organization_id,
    )


def get_parent_hierarchies(
    *,
    child_organization_id,
) -> QuerySet[OrganizationHierarchy]:
    """
    Return all parent hierarchy relationships.
    """

    return OrganizationHierarchy.objects.with_related().by_child(
        child_organization_id,
    )


def search_organization_hierarchies(
    *,
    query: str,
) -> QuerySet[OrganizationHierarchy]:
    """
    Search organization hierarchies.
    """

    return OrganizationHierarchy.objects.with_related().search(
        query,
    )


__all__ = [
    "get_organization_hierarchy_by_id",
    "get_organization_hierarchies",
    "get_child_hierarchies",
    "get_parent_hierarchies",
    "search_organization_hierarchies",
]
