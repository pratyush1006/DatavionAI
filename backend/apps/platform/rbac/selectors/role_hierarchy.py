"""
Role hierarchy selectors.
"""

from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    RoleHierarchy,
)


def get_role_hierarchies():
    """
    Return all role hierarchies.
    """

    return RoleHierarchy.objects.with_related()


def get_role_hierarchy_by_id(
    *,
    role_hierarchy_id: int,
) -> RoleHierarchy:
    """
    Return a role hierarchy by id.
    """

    return get_object_or_404(
        RoleHierarchy.objects.with_related(),
        pk=role_hierarchy_id,
    )


def get_active_role_hierarchies():
    """
    Return active role hierarchies.
    """

    return RoleHierarchy.objects.active().with_related()


def get_inactive_role_hierarchies():
    """
    Return inactive role hierarchies.
    """

    return RoleHierarchy.objects.inactive().with_related()


def get_parent_role_hierarchies(
    *,
    role_id: int,
):
    """
    Return hierarchies where the given role is the parent.
    """

    return RoleHierarchy.objects.for_parent_role(
        role_id,
    ).with_related()


def get_child_role_hierarchies(
    *,
    role_id: int,
):
    """
    Return hierarchies where the given role is the child.
    """

    return RoleHierarchy.objects.for_child_role(
        role_id,
    ).with_related()


def get_direct_role_hierarchies():
    """
    Return direct role hierarchies.
    """

    return RoleHierarchy.objects.direct().with_related()


def get_inherited_role_hierarchies():
    """
    Return inherited role hierarchies.
    """

    return RoleHierarchy.objects.inherited().with_related()


def search_role_hierarchies(
    *,
    query: str,
):
    """
    Search role hierarchies.
    """

    return RoleHierarchy.objects.search(query).with_related()


__all__ = [
    "get_active_role_hierarchies",
    "get_child_role_hierarchies",
    "get_direct_role_hierarchies",
    "get_inactive_role_hierarchies",
    "get_inherited_role_hierarchies",
    "get_parent_role_hierarchies",
    "get_role_hierarchies",
    "get_role_hierarchy_by_id",
    "search_role_hierarchies",
]
