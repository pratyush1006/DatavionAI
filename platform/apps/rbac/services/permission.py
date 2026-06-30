"""
Write services for Permission.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import Permission


@transaction.atomic
def create_permission(
    *,
    name: str,
    code: str,
    description: str = "",
    is_active: bool = True,
) -> Permission:
    """
    Create a new permission.
    """

    return Permission.objects.create(
        name=name,
        code=code,
        description=description,
        is_active=is_active,
    )


@transaction.atomic
def update_permission(
    *,
    permission: Permission,
    name: str,
    code: str,
    description: str,
    is_active: bool,
) -> Permission:
    """
    Update an existing permission.
    """

    permission.name = name
    permission.code = code
    permission.description = description
    permission.is_active = is_active

    permission.save(
        update_fields=[
            "name",
            "code",
            "description",
            "is_active",
            "updated_at",
        ],
    )

    return permission


@transaction.atomic
def delete_permission(
    *,
    permission: Permission,
) -> None:
    """
    Delete a permission.
    """

    permission.delete()
