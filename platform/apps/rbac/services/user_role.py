"""
Write services for UserRole.
"""

from __future__ import annotations

from django.db import transaction

from apps.accounts.models import User
from apps.rbac.models import Role, UserRole


@transaction.atomic
def assign_role_to_user(
    *,
    user: User,
    role: Role,
) -> UserRole:
    """
    Assign a role to a user.

    If the assignment already exists, return it.
    """

    user_role, _ = UserRole.objects.get_or_create(
        user=user,
        role=role,
    )

    return user_role


@transaction.atomic
def remove_role_from_user(
    *,
    user: User,
    role: Role,
) -> None:
    """
    Remove a role from a user.
    """

    UserRole.objects.filter(
        user=user,
        role=role,
    ).delete()
