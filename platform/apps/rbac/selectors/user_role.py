"""
Read-only selectors for UserRole.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.rbac.models import UserRole

_USER_ROLE_LIST_FIELDS = (
    "id",
    "user",
    "role",
)


def get_user_roles() -> QuerySet[UserRole]:
    """
    Return all user-role assignments.
    """

    return (
        UserRole.objects.select_related(
            "user",
            "role",
        )
        .only(
            *_USER_ROLE_LIST_FIELDS,
        )
        .order_by(
            "user__id",
            "role__name",
        )
    )


def get_user_role_by_id(
    *,
    user_role_id: int,
) -> UserRole:
    """
    Return a user-role assignment by its primary key.
    """

    return get_object_or_404(
        get_user_roles(),
        pk=user_role_id,
    )


def get_roles_for_user(
    *,
    user_id: int,
) -> QuerySet[UserRole]:
    """
    Return all role assignments for a user.
    """

    return get_user_roles().filter(
        user_id=user_id,
    )


def get_users_for_role(
    *,
    role_id: int,
) -> QuerySet[UserRole]:
    """
    Return all users assigned to a role.
    """

    return get_user_roles().filter(
        role_id=role_id,
    )
