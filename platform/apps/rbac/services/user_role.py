"""
Write services for UserRole.
"""

from __future__ import annotations

from django.db import transaction

from apps.rbac.models import UserRole


@transaction.atomic
def assign_role_to_user(
    *,
    validated_data: dict,
) -> UserRole:
    """
    Assign a role to a user.

    If the assignment already exists,
    return the existing assignment.
    """

    user_role, _ = UserRole.objects.get_or_create(
        **validated_data,
    )

    return user_role


@transaction.atomic
def remove_role_from_user(
    *,
    instance: UserRole,
) -> None:
    """
    Remove a role assignment.
    """

    instance.delete()
