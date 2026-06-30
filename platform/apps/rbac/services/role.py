"""
Write services for Role.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import Role


@transaction.atomic
def create_role(
    *,
    name: str,
    code: str,
    description: str = "",
    is_active: bool = True,
) -> Role:
    """
    Create a new role.
    """

    return Role.objects.create(
        name=name,
        code=code,
        description=description,
        is_active=is_active,
    )


@transaction.atomic
def update_role(
    *,
    role: Role,
    name: str,
    code: str,
    description: str,
    is_active: bool,
) -> Role:
    """
    Update an existing role.
    """

    role.name = name
    role.code = code
    role.description = description
    role.is_active = is_active

    role.save(
        update_fields=[
            "name",
            "code",
            "description",
            "is_active",
            "updated_at",
        ],
    )

    return role


@transaction.atomic
def delete_role(
    *,
    role: Role,
) -> None:
    """
    Delete a role.
    """

    role.delete()
