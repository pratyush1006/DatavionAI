"""
Write services for Role.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import Role


@transaction.atomic
def create_role(
    *,
    validated_data: dict,
) -> Role:
    """
    Create a new role.
    """

    return Role.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_role(
    *,
    instance: Role,
    validated_data: dict,
) -> Role:
    """
    Update an existing role.
    """

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save()

    return instance


@transaction.atomic
def delete_role(
    *,
    instance: Role,
) -> None:
    """
    Delete a role.
    """

    instance.delete()
