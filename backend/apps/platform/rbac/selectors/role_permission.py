"""
Role permission selectors.
"""

from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.platform.rbac.models import (
    RolePermission,
)


def get_role_permission_by_id(
    *,
    role_permission_id,
) -> RolePermission:
    """
    Return a role permission by its identifier.
    """

    return get_object_or_404(
        RolePermission.objects.with_related(),
        pk=role_permission_id,
    )


def get_role_permissions():
    """
    Return all active role permissions.
    """

    return RolePermission.objects.with_related().active()


def get_role_permissions_for_role(
    *,
    role=None,
    role_id=None,
):
    """
    Return permissions assigned to a role.

    Accepts either a Role instance or a role_id for
    backward compatibility.
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
):
    """
    Return role permissions for a permission.

    Accepts either a Permission instance or a permission_id
    for backward compatibility.
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


def get_direct_role_permissions():
    """
    Return directly assigned role permissions.
    """

    return RolePermission.objects.direct().active().with_related()


def get_inherited_role_permissions():
    """
    Return inherited role permissions.
    """

    return RolePermission.objects.inherited().active().with_related()


def search_role_permissions(
    *,
    query: str,
):
    """
    Search role permissions.
    """

    return RolePermission.objects.search(
        query,
    ).with_related()


__all__ = [
    "get_direct_role_permissions",
    "get_inherited_role_permissions",
    "get_role_permission_by_id",
    "get_role_permissions",
    "get_role_permissions_for_permission",
    "get_role_permissions_for_role",
    "search_role_permissions",
]
