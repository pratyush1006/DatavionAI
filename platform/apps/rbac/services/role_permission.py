"""
Write services for RolePermission.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import RolePermission


@transaction.atomic
def assign_permission_to_role(
    *,
    validated_data: dict,
) -> RolePermission:
    """
    Assign a permission to a role.

    If the assignment already exists,
    return the existing assignment.
    """

    role_permission, _ = RolePermission.objects.get_or_create(
        **validated_data,
    )

    return role_permission


@transaction.atomic
def remove_permission_from_role(
    *,
    instance: RolePermission,
) -> None:
    """
    Remove a role-permission assignment.
    """

    instance.delete()
