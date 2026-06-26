from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.shortcuts import get_object_or_404

from apps.accounts.models import User


# ======================================================
# Role Selectors
# ======================================================

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
    Return a single role.
    """
    return get_object_or_404(
        Group.objects.prefetch_related(
            "permissions"
        ),
        id=role_id,
    )


# ======================================================
# User Selectors
# ======================================================

def get_user_by_id(user_id):
    """
    Return a single user.
    """
    return get_object_or_404(
        User.objects.prefetch_related(
            "groups"
        ),
        id=user_id,
    )


# ======================================================
# Permission Selectors
# ======================================================

def get_permissions():
    """
    Return all permissions.
    """
    return (
        Permission.objects
        .select_related("content_type")
        .order_by(
            "content_type__app_label",
            "codename",
        )
    )


def get_permission_by_id(permission_id):
    """
    Return one permission.
    """
    return get_object_or_404(
        Permission.objects.select_related(
            "content_type"
        ),
        id=permission_id,
    )


def get_permissions_by_ids(permission_ids):
    """
    Return multiple permissions.
    """
    return Permission.objects.filter(
        id__in=permission_ids
    )