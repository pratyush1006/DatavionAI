"""
Selectors for PermissionGroup.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    PermissionGroup,
)


def get_permission_group_by_id(
    *,
    permission_group_id,
) -> PermissionGroup:
    """
    Return a permission group by its identifier.
    """

    return get_object_or_404(
        PermissionGroup.objects,
        id=permission_group_id,
    )


def get_permission_group_by_code(
    *,
    code: str,
) -> PermissionGroup:
    """
    Return a permission group by its code.
    """

    return get_object_or_404(
        PermissionGroup.objects,
        code=code,
    )


def get_permission_groups() -> QuerySet[PermissionGroup]:
    """
    Return active permission groups.
    """

    return PermissionGroup.objects.active().ordered()


def get_inactive_permission_groups() -> QuerySet[PermissionGroup]:
    """
    Return inactive permission groups.
    """

    return PermissionGroup.objects.inactive().ordered()


def get_system_permission_groups() -> QuerySet[PermissionGroup]:
    """
    Return system permission groups.
    """

    return PermissionGroup.objects.system().ordered()


def get_custom_permission_groups() -> QuerySet[PermissionGroup]:
    """
    Return custom permission groups.
    """

    return PermissionGroup.objects.custom().ordered()


def get_permission_groups_by_module(
    *,
    module: str,
) -> QuerySet[PermissionGroup]:
    """
    Return permission groups for a module.
    """

    return PermissionGroup.objects.by_module(
        module,
    ).ordered()


def search_permission_groups(
    *,
    query: str,
) -> QuerySet[PermissionGroup]:
    """
    Search permission groups.
    """

    return PermissionGroup.objects.search(
        query,
    ).ordered()


__all__ = [
    "get_custom_permission_groups",
    "get_inactive_permission_groups",
    "get_permission_group_by_code",
    "get_permission_group_by_id",
    "get_permission_groups",
    "get_permission_groups_by_module",
    "get_system_permission_groups",
    "search_permission_groups",
]
