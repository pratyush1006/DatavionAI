"""
Organization role selectors.
"""

from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    OrganizationRole,
)


def get_organization_roles():
    """
    Return all organization roles.
    """

    return OrganizationRole.objects.with_related()


def get_organization_role_by_id(
    *,
    organization_role_id: int,
) -> OrganizationRole:
    """
    Return an organization role by id.
    """

    return get_object_or_404(
        OrganizationRole.objects.with_related(),
        pk=organization_role_id,
    )


def get_organization_roles_for_organization(
    *,
    organization_id: int,
):
    """
    Return organization roles for an organization.
    """

    return OrganizationRole.objects.for_organization(
        organization_id,
    ).with_related()


def get_organization_roles_for_user(
    *,
    user_id: int,
):
    """
    Return organization roles for a user.
    """

    return OrganizationRole.objects.for_user(
        user_id,
    ).with_related()


def get_organization_roles_for_role(
    *,
    role_id: int,
):
    """
    Return organization roles for a role.
    """

    return OrganizationRole.objects.for_role(
        role_id,
    ).with_related()


def get_active_organization_roles():
    """
    Return active organization roles.
    """

    return OrganizationRole.objects.active().with_related()


def get_inactive_organization_roles():
    """
    Return inactive organization roles.
    """

    return OrganizationRole.objects.inactive().with_related()


def get_primary_organization_roles():
    """
    Return primary organization roles.
    """

    return OrganizationRole.objects.primary().with_related()


def search_organization_roles(
    *,
    query: str,
):
    """
    Search organization roles.
    """

    return OrganizationRole.objects.search(query).with_related()


__all__ = [
    "get_active_organization_roles",
    "get_inactive_organization_roles",
    "get_organization_role_by_id",
    "get_organization_roles",
    "get_organization_roles_for_organization",
    "get_organization_roles_for_role",
    "get_organization_roles_for_user",
    "get_primary_organization_roles",
    "search_organization_roles",
]
