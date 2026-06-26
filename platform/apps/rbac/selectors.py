from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from apps.accounts.models import User


def get_roles():
    """
    Return all roles.
    """
    return (
        Group.objects
        .prefetch_related("permissions")
        .order_by("name")
    )


def get_role_by_id(role_id):
    """
    Return a single role by id.
    """
    return get_object_or_404(
        Group.objects.prefetch_related("permissions"),
        id=role_id,
    )


def get_user_by_id(user_id):
    """
    Return a user with assigned groups.
    """
    return get_object_or_404(
        User.objects.prefetch_related("groups"),
        id=user_id,
    )