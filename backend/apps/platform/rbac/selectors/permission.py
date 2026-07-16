"""
Selectors for Permission.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    Permission,
)


def get_permission_by_id(
    *,
    permission_id,
) -> Permission:
    """
    Return a permission by its identifier.
    """

    return get_object_or_404(
        Permission.objects,
        id=permission_id,
    )


def get_permission_by_code(
    *,
    code: str,
) -> Permission:
    """
    Return a permission by its code.
    """

    return get_object_or_404(
        Permission.objects,
        code=code,
    )


def get_permissions() -> QuerySet[Permission]:
    """
    Return active permissions.
    """

    return Permission.objects.active().ordered()


def get_inactive_permissions() -> QuerySet[Permission]:
    """
    Return inactive permissions.
    """

    return Permission.objects.inactive().ordered()


def get_system_permissions() -> QuerySet[Permission]:
    """
    Return built-in permissions.
    """

    return Permission.objects.system().ordered()


def get_custom_permissions() -> QuerySet[Permission]:
    """
    Return custom permissions.
    """

    return Permission.objects.custom().ordered()


def get_assignable_permissions() -> QuerySet[Permission]:
    """
    Return assignable permissions.
    """

    return Permission.objects.assignable().ordered()


def get_delegable_permissions() -> QuerySet[Permission]:
    """
    Return delegable permissions.
    """

    return Permission.objects.delegable().ordered()


def get_permissions_by_module(
    *,
    module: str,
) -> QuerySet[Permission]:
    """
    Return permissions for a module.
    """

    return Permission.objects.by_module(
        module,
    ).ordered()


def get_permissions_by_action(
    *,
    action: str,
) -> QuerySet[Permission]:
    """
    Return permissions for an action.
    """

    return Permission.objects.by_action(
        action,
    ).ordered()


def get_permissions_by_scope(
    *,
    scope: str,
) -> QuerySet[Permission]:
    """
    Return permissions for a scope.
    """

    return Permission.objects.by_scope(
        scope,
    ).ordered()


def search_permissions(
    *,
    query: str,
) -> QuerySet[Permission]:
    """
    Search permissions.
    """

    return Permission.objects.search(
        query,
    ).ordered()


__all__ = [
    "get_assignable_permissions",
    "get_custom_permissions",
    "get_delegable_permissions",
    "get_inactive_permissions",
    "get_permission_by_code",
    "get_permission_by_id",
    "get_permissions",
    "get_permissions_by_action",
    "get_permissions_by_module",
    "get_permissions_by_scope",
    "get_system_permissions",
    "search_permissions",
]
