"""
Read-only selectors for the Accounts application.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.accounts.models import (
    Profile,
    User,
)

type UserQuerySet = QuerySet[User]
type ProfileQuerySet = QuerySet[Profile]


USER_LIST_FIELDS = (
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
) -> UserQuerySet:
    """
    Return users ordered by email.
    """

    queryset = (
        User.objects.select_related(
            "profile",
        )
        .only(
            *USER_LIST_FIELDS,
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
    Return a user by primary key.
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
    Return a user by email.
    """

    return get_object_or_404(
        get_users(
            include_inactive=True,
        ),
        email=email,
    )


def get_profiles() -> ProfileQuerySet:
    """
    Return all profiles.
    """

    return Profile.objects.select_related(
        "user",
    ).order_by(
        "user__email",
    )


def get_profile_by_id(
    *,
    profile_id: int,
) -> Profile:
    """
    Return a profile by primary key.
    """

    return get_object_or_404(
        get_profiles(),
        pk=profile_id,
    )


def get_profile_by_user(
    *,
    user: User,
) -> Profile:
    """
    Return the profile for a user.
    """

    return get_object_or_404(
        get_profiles(),
        user=user,
    )


__all__ = [
    "get_users",
    "get_user_by_id",
    "get_user_by_email",
    "get_profiles",
    "get_profile_by_id",
    "get_profile_by_user",
]
