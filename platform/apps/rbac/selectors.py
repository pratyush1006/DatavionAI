from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


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