"""
Read-only selectors for the Accounts app.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.accounts.models import (
    Profile,
    User,
)

_USER_LIST_FIELDS = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_active",
    "is_verified",
)


def get_users(
    *,
    include_inactive: bool = False,
) -> QuerySet[User]:
    """
    Return users ordered by email.

    By default, only active users are returned.
    """

    queryset = (
        User.objects.select_related(
            "profile",
        )
        .only(
            *_USER_LIST_FIELDS,
        )
        .order_by(
            "email",
        )
    )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset


def get_user_by_id(
    *,
    user_id: int,
) -> User:
    """
    Return a single user by its primary key.
    """

    return get_object_or_404(
        get_users(
            include_inactive=True,
        ),
        pk=user_id,
    )


def get_user_by_email(
    *,
    email: str,
) -> User:
    """
    Return a single user by email.
    """

    return get_object_or_404(
        User.objects.select_related(
            "profile",
        ),
        email=email,
    )


def get_profile_by_user(
    *,
    user: User,
) -> Profile:
    """
    Return the profile associated with a user.
    """

    return get_object_or_404(
        Profile,
        user=user,
    )


def get_profile_by_id(
    *,
    profile_id: int,
) -> Profile:
    """
    Return a single profile by its primary key.
    """

    return get_object_or_404(
        Profile.objects.select_related(
            "user",
        ),
        pk=profile_id,
    )
