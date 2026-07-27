"""
Role permission selectors.

Read-only query layer for RBAC role permission assignments.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    RolePermission,
)

type RolePermissionQuerySet = QuerySet[RolePermission]


def get_role_permission_by_id(
    *,
    role_permission_id,
) -> RolePermission:
    """
    Return a role permission by identifier.
    """

    return get_object_or_404(
        RolePermission.objects.with_related(),
        pk=role_permission_id,
    )


def get_role_permissions() -> RolePermissionQuerySet:
    """
    Return active role permissions.
    """

    return RolePermission.objects.with_related().active()


def get_role_permissions_for_role(
    *,
    role=None,
    role_id=None,
) -> RolePermissionQuerySet:
    """
    Return permissions assigned to a role.

    Supports:
    - Role instance
    - Role identifier
    """

    if role_id is None:
        if role is None:
            raise ValueError(
                "Either 'role' or 'role_id' must be provided.",
            )

        role_id = role.id

    return (
        RolePermission.objects.with_related()
        .for_role(
            role_id,
        )
        .active()
    )


def get_role_permissions_for_permission(
    *,
    permission=None,
    permission_id=None,
) -> RolePermissionQuerySet:
    """
    Return roles assigned to a permission.

    Supports:
    - Permission instance
    - Permission identifier
    """

    if permission_id is None:
        if permission is None:
            raise ValueError(
                "Either 'permission' or 'permission_id' must be provided.",
            )

        permission_id = permission.id

    return (
        RolePermission.objects.with_related()
        .for_permission(
            permission_id,
        )
        .active()
    )


def get_direct_role_permissions() -> RolePermissionQuerySet:
    """
    Return directly assigned permissions.
    """

    return RolePermission.objects.direct().active().with_related()


def get_inherited_role_permissions() -> RolePermissionQuerySet:
    """
    Return inherited permissions.
    """

    return RolePermission.objects.inherited().active().with_related()


def search_role_permissions(
    *,
    query: str,
) -> RolePermissionQuerySet:
    """
    Search role permissions.
    """

    return (
        RolePermission.objects.search(
            query,
        )
        .active()
        .with_related()
    )


__all__ = [
    "RolePermissionQuerySet",
    "get_direct_role_permissions",
    "get_inherited_role_permissions",
    "get_role_permission_by_id",
    "get_role_permissions",
    "get_role_permissions_for_permission",
    "get_role_permissions_for_role",
    "search_role_permissions",
]
