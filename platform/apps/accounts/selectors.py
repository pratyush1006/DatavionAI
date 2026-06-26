from django.shortcuts import get_object_or_404

from apps.accounts.models import User


def get_users():
    """
    Return all users.
    """
    return (
        User.objects
        .select_related("organization")
        .order_by("username")
    )


def get_user_by_id(user_id):
    """
    Return a single user by id.
    """
    return get_object_or_404(
        User.objects.select_related("organization"),
        id=user_id,
    )