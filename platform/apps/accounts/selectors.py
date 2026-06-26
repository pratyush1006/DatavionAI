from django.shortcuts import get_object_or_404

from apps.accounts.models import User


def get_users(user):
    """
    Return users visible to the current user.

    Superusers can see every user.
    Other users can only see users in their organization.
    """

    queryset = User.objects.select_related("organization").order_by("username")

    if user.is_superuser:
        return queryset

    return queryset.filter(organization=user.organization)


def get_user_by_id(user_id, user):
    """
    Return a single user visible to the current user.
    """

    queryset = User.objects.select_related("organization")

    if user.is_superuser:
        return get_object_or_404(
            queryset,
            id=user_id,
        )

    return get_object_or_404(
        queryset,
        id=user_id,
        organization=user.organization,
    )
