"""
Write services for Permission.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import Permission


@transaction.atomic
def create_permission(
    *,
    validated_data: dict,
) -> Permission:
    """
    Create a new permission.
    """

    return Permission.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_permission(
    *,
    instance: Permission,
    validated_data: dict,
) -> Permission:
    """
    Update an existing permission.
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
def delete_permission(
    *,
    instance: Permission,
) -> None:
    """
    Delete a permission.
    """

    instance.delete()
