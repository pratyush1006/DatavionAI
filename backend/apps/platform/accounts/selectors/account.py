"""
Read-only selectors for the Accounts application.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.platform.accounts.models import (
    Profile,
    User,
)

type UserQuerySet = QuerySet[User]
type ProfileQuerySet = QuerySet[Profile]


def get_users(
    *,
    include_inactive: bool = False,
) -> UserQuerySet:
    """
    Return users ordered by email.

    Related objects are eagerly loaded to avoid N+1 queries.
    """

    queryset = User.objects.select_related(
        "profile",
        "organization",
    ).order_by(
        "email",
    )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset


def get_active_users() -> UserQuerySet:
    """
    Return active users.
    """

    return get_users()


def get_verified_users() -> UserQuerySet:
    """
    Return verified users.
    """

    return get_users().filter(
        is_verified=True,
    )


def get_unverified_users() -> UserQuerySet:
    """
    Return users whose email has not yet been verified.
    """

    return get_users(
        include_inactive=True,
    ).filter(
        is_verified=False,
    )


def get_user_by_id(
    *,
    user_id: UUID,
) -> User | None:
    """
    Return a user by ID.
    """

    return (
        get_users(
            include_inactive=True,
        )
        .filter(
            pk=user_id,
        )
        .first()
    )


def get_user_by_email(
    *,
    email: str,
) -> User | None:
    """
    Return a user by email.
    """

    return (
        get_users(
            include_inactive=True,
        )
        .filter(
            email=email.strip().lower(),
        )
        .first()
    )


def search_users(
    *,
    query: str,
) -> UserQuerySet:
    """
    Search users by email.
    """

    return get_users(
        include_inactive=True,
    ).filter(
        email__icontains=query.strip(),
    )


def get_profiles() -> ProfileQuerySet:
    """
    Return all profiles ordered by user email.
    """

    return Profile.objects.select_related(
        "user",
    ).order_by(
        "user__email",
    )


def get_profile_by_id(
    *,
    profile_id: UUID,
) -> Profile | None:
    """
    Return a profile by ID.
    """

    return (
        get_profiles()
        .filter(
            pk=profile_id,
        )
        .first()
    )


def get_profile_by_user(
    *,
    user: User,
) -> Profile | None:
    """
    Return a user's profile.
    """

    return (
        get_profiles()
        .filter(
            user=user,
        )
        .first()
    )


__all__ = [
    "get_active_users",
    "get_profiles",
    "get_profile_by_id",
    "get_profile_by_user",
    "get_unverified_users",
    "get_user_by_email",
    "get_user_by_id",
    "get_users",
    "get_verified_users",
    "search_users",
]
