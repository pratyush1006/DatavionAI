"""
User role selectors.
"""

from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    UserRole,
)


def get_user_role_by_id(
    *,
    user_role_id,
) -> UserRole:
    """
    Return a user role by its identifier.
    """

    return get_object_or_404(
        UserRole.objects.with_related(),
        pk=user_role_id,
    )


def get_user_roles():
    """
    Return all user roles.
    """

    return UserRole.objects.with_related().active()


def get_user_roles_for_user(
    *,
    user,
):
    """
    Return roles assigned to a user.
    """

    return (
        UserRole.objects.with_related()
        .for_user(
            user.id,
        )
        .active()
    )


def get_user_roles_for_role(
    *,
    role,
):
    """
    Return users assigned to a role.
    """

    return (
        UserRole.objects.with_related()
        .for_role(
            role.id,
        )
        .active()
    )


def search_user_roles(
    *,
    query: str,
):
    """
    Search user role assignments.
    """

    return UserRole.objects.search(
        query,
    ).with_related()


__all__ = [
    "get_user_role_by_id",
    "get_user_roles",
    "get_user_roles_for_role",
    "get_user_roles_for_user",
    "search_user_roles",
]
