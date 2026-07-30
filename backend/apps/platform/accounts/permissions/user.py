"""
User permissions for DatavionOS Accounts.

Implements SaaS tenant-aware RBAC rules.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    """
    Base authentication permission.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return bool(
            request.user and request.user.is_authenticated,
        )


class CanViewUser(IsAuthenticatedUser):
    """
    Permission to view users.

    Allowed:
    - Platform admins
    - Tenant admins
    - Organization admins
    - User viewing self
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:

        user = request.user

        if user.is_superuser:
            return True

        if obj.id == user.id:
            return True

        if getattr(
            user,
            "is_staff",
            False,
        ):
            return True

        return bool(
            getattr(user, "organization_id", None)
            and user.organization_id == obj.organization_id
        )


class CanCreateUser(IsAuthenticatedUser):
    """
    Permission to create users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        user = request.user

        if user.is_superuser:
            return True

        return bool(
            getattr(
                user,
                "is_staff",
                False,
            )
        )


class CanUpdateUser(IsAuthenticatedUser):
    """
    Permission to update users.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:

        user = request.user

        if user.is_superuser:
            return True

        if obj.id == user.id:
            return True

        return bool(
            getattr(
                user,
                "is_staff",
                False,
            )
            and user.organization_id == obj.organization_id
        )


class CanDeleteUser(IsAuthenticatedUser):
    """
    Permission to deactivate users.

    Permanent deletion should not happen
    in healthcare SaaS.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:

        user = request.user

        if user.is_superuser:
            return True

        return bool(
            getattr(
                user,
                "is_staff",
                False,
            )
            and user.organization_id == obj.organization_id
        )


__all__ = (
    "CanCreateUser",
    "CanDeleteUser",
    "CanUpdateUser",
    "CanViewUser",
    "IsAuthenticatedUser",
)
