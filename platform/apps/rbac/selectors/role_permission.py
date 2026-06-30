"""
Read-only selectors for RolePermission.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.rbac.models import RolePermission

_ROLE_PERMISSION_LIST_FIELDS = (
    "id",
    "role",
    "permission",
)


def get_role_permissions() -> QuerySet[RolePermission]:
    """
    Return all role-permission assignments.
    """

    return (
        RolePermission.objects.select_related(
            "role",
            "permission",
        )
        .only(
            *_ROLE_PERMISSION_LIST_FIELDS,
        )
        .order_by(
            "role__name",
            "permission__name",
        )
    )


def get_role_permission_by_id(
    *,
    role_permission_id: int,
) -> RolePermission:
    """
    Return a role-permission assignment by primary key.
    """

    return get_object_or_404(
        get_role_permissions(),
        pk=role_permission_id,
    )


def get_permissions_for_role(
    *,
    role_id: int,
) -> QuerySet[RolePermission]:
    """
    Return all permissions assigned to a role.
    """

    return get_role_permissions().filter(
        role_id=role_id,
    )


def get_roles_for_permission(
    *,
    permission_id: int,
) -> QuerySet[RolePermission]:
    """
    Return all roles assigned to a permission.
    """

    return get_role_permissions().filter(
        permission_id=permission_id,
    )
