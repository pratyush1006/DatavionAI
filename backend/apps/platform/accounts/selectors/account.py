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
    tenant=None,
    organization=None,
    include_inactive: bool = False,
) -> UserQuerySet:
    """
    Return users scoped to tenant and organization.
    """

    queryset = User.objects.select_related(
        "profile",
        "organization",
    ).order_by(
        "email",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    elif tenant is not None:
        queryset = queryset.filter(
            organization__tenant=tenant,
        )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset


def get_active_users(
    *,
    tenant=None,
    organization=None,
) -> UserQuerySet:
    """
    Return active users.
    """

    return get_users(
        tenant=tenant,
        organization=organization,
    )


def get_verified_users(
    *,
    tenant=None,
    organization=None,
) -> UserQuerySet:
    """
    Return verified users.
    """

    return get_users(
        tenant=tenant,
        organization=organization,
    ).filter(
        is_verified=True,
    )


def get_unverified_users(
    *,
    tenant=None,
    organization=None,
) -> UserQuerySet:
    """
    Return unverified users.
    """

    return get_users(
        tenant=tenant,
        organization=organization,
        include_inactive=True,
    ).filter(
        is_verified=False,
    )


def get_user_by_id(
    *,
    user_id: UUID,
    tenant=None,
    organization=None,
) -> User | None:
    """
    Return user by UUID.
    """

    return (
        get_users(
            tenant=tenant,
            organization=organization,
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
    Global email lookup.

    Required for authentication before
    tenant resolution.
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
    tenant=None,
    organization=None,
) -> UserQuerySet:
    """
    Search users inside tenant boundary.
    """

    return get_users(
        tenant=tenant,
        organization=organization,
        include_inactive=True,
    ).filter(
        email__icontains=query.strip(),
    )


def get_profiles(
    *,
    tenant=None,
    organization=None,
) -> ProfileQuerySet:
    """
    Return tenant scoped profiles.
    """

    queryset = Profile.objects.select_related(
        "user",
        "user__organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            user__organization=organization,
        )

    elif tenant is not None:
        queryset = queryset.filter(
            user__organization__tenant=tenant,
        )

    return queryset.order_by(
        "user__email",
    )


def get_profile_by_id(
    *,
    profile_id: UUID,
    tenant=None,
    organization=None,
) -> Profile | None:
    """
    Return profile by UUID.
    """

    return (
        get_profiles(
            tenant=tenant,
            organization=organization,
        )
        .filter(
            pk=profile_id,
        )
        .first()
    )


def get_profile_by_user(
    *,
    user: User,
    tenant=None,
    organization=None,
) -> Profile | None:
    """
    Return profile by user.
    """

    return (
        get_profiles(
            tenant=tenant,
            organization=organization,
        )
        .filter(
            user=user,
        )
        .first()
    )


__all__ = (
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
)
