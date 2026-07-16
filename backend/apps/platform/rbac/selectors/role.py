"""
Selectors for Role.
"""

from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    Role,
)


def get_role_by_id(
    *,
    role_id,
) -> Role:
    """
    Return a role by its identifier.
    """

    return get_object_or_404(
        Role.objects.select_related(
            "parent",
        ),
        id=role_id,
    )


def get_role_by_code(
    *,
    code: str,
) -> Role:
    """
    Return a role by its code.
    """

    return get_object_or_404(
        Role.objects.select_related(
            "parent",
        ),
        code=code,
    )


def get_roles():
    """
    Return all roles.
    """

    return Role.objects.ordered().select_related(
        "parent",
    )


def get_active_roles():
    """
    Return active roles.
    """

    return (
        Role.objects.active()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_inactive_roles():
    """
    Return inactive roles.
    """

    return (
        Role.objects.inactive()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_system_roles():
    """
    Return built-in platform roles.
    """

    return (
        Role.objects.system()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_custom_roles():
    """
    Return custom roles.
    """

    return (
        Role.objects.custom()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_default_roles():
    """
    Return default roles.
    """

    return (
        Role.objects.defaults()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_assignable_roles():
    """
    Return assignable roles.
    """

    return (
        Role.objects.assignable()
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_roles_by_type(
    *,
    role_type: str,
):
    """
    Return roles for a role type.
    """

    return (
        Role.objects.by_type(
            role_type,
        )
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_roles_by_scope(
    *,
    scope: str,
):
    """
    Return roles for a scope.
    """

    return (
        Role.objects.by_scope(
            scope,
        )
        .ordered()
        .select_related(
            "parent",
        )
    )


def get_roles_by_category(
    *,
    category: str,
):
    """
    Return roles for a category.
    """

    return (
        Role.objects.by_category(
            category,
        )
        .ordered()
        .select_related(
            "parent",
        )
    )


def search_roles(
    *,
    query: str,
):
    """
    Search roles.
    """

    return (
        Role.objects.search(
            query,
        )
        .ordered()
        .select_related(
            "parent",
        )
    )


__all__ = [
    "get_active_roles",
    "get_assignable_roles",
    "get_custom_roles",
    "get_default_roles",
    "get_inactive_roles",
    "get_role_by_code",
    "get_role_by_id",
    "get_roles",
    "get_roles_by_category",
    "get_roles_by_scope",
    "get_roles_by_type",
    "get_system_roles",
    "search_roles",
]
