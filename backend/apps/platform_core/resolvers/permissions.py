"""
Permission resolver.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


class PermissionResolver:
    """
    Resolve platform permissions for a user.
    """

    def resolve(
        self,
        user: User,
    ) -> set[str]:
        """
        Return all effective permissions for the user.
        """

        if not user.is_authenticated:
            return set()

        if user.is_superuser:
            return {
                permission.split(".", 1)[1] if "." in permission else permission
                for permission in user.get_all_permissions()
            }

        return {
            permission.split(".", 1)[1] if "." in permission else permission
            for permission in user.get_all_permissions()
        }

    def has_permission(
        self,
        *,
        user: User,
        permission: str,
    ) -> bool:
        """
        Check whether a user has a permission.
        """

        return permission in self.resolve(
            user=user,
        )

    def has_any_permission(
        self,
        *,
        user: User,
        permissions: set[str],
    ) -> bool:
        """
        Check whether the user has at least one permission.
        """

        user_permissions = self.resolve(
            user=user,
        )

        return bool(
            user_permissions.intersection(
                permissions,
            ),
        )

    def has_all_permissions(
        self,
        *,
        user: User,
        permissions: set[str],
    ) -> bool:
        """
        Check whether the user has every permission.
        """

        user_permissions = self.resolve(
            user=user,
        )

        return permissions.issubset(
            user_permissions,
        )


permission_resolver = PermissionResolver()


__all__ = [
    "PermissionResolver",
    "permission_resolver",
]
