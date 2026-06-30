"""
Write services for RolePermission.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import Permission, Role, RolePermission


@transaction.atomic
def assign_permission_to_role(
    *,
    role: Role,
    permission: Permission,
) -> RolePermission:
    """
    Assign a permission to a role.

    If the assignment already exists, return it.
    """

    role_permission, _ = RolePermission.objects.get_or_create(
        role=role,
        permission=permission,
    )

    return role_permission


@transaction.atomic
def remove_permission_from_role(
    *,
    role: Role,
    permission: Permission,
) -> None:
    """
    Remove a permission from a role.
    """

    RolePermission.objects.filter(
        role=role,
        permission=permission,
    ).delete()
