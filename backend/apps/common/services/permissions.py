"""
DatavionAI Service Permissions.

Reusable authorization helpers for enterprise services.

Design Principles
-----------------
- Framework agnostic
- RBAC friendly
- Stateless
- Exception framework integration
"""

from __future__ import annotations

from typing import Any

from apps.common.exceptions.builders import permission_denied


class PermissionService:
    """
    Shared authorization helpers.
    """

    @staticmethod
    def require(
        condition: bool,
        *,
        message: str | None = None,
    ) -> None:
        """
        Ensure a permission condition is satisfied.
        """

        if not condition:
            raise permission_denied(
                message=message,
            )

    @staticmethod
    def require_authenticated(
        user: Any | None,
    ) -> Any:
        """
        Ensure the user is authenticated.
        """

        if user is None or not getattr(user, "is_authenticated", False):
            raise permission_denied(
                message="Authentication required.",
            )

        return user

    @staticmethod
    def require_active(
        user: Any,
    ) -> Any:
        """
        Ensure the user account is active.
        """

        if not getattr(user, "is_active", False):
            raise permission_denied(
                message="User account is inactive.",
            )

        return user

    @staticmethod
    def require_staff(
        user: Any,
    ) -> Any:
        """
        Ensure the user is a staff member.
        """

        if not getattr(user, "is_staff", False):
            raise permission_denied(
                message="Staff access required.",
            )

        return user

    @staticmethod
    def require_superuser(
        user: Any,
    ) -> Any:
        """
        Ensure the user is a superuser.
        """

        if not getattr(user, "is_superuser", False):
            raise permission_denied(
                message="Superuser access required.",
            )

        return user

    @staticmethod
    def require_permission(
        user: Any,
        permission: str,
    ) -> None:
        """
        Ensure the user has the specified permission.
        """

        if not user.has_perm(permission):
            raise permission_denied(
                message=f"Missing permission: {permission}",
            )

    @staticmethod
    def require_any_permission(
        user: Any,
        *permissions: str,
    ) -> None:
        """
        Ensure the user has at least one permission.
        """

        if not any(user.has_perm(permission) for permission in permissions):
            raise permission_denied(
                message="Required permission not granted.",
            )

    @staticmethod
    def require_all_permissions(
        user: Any,
        *permissions: str,
    ) -> None:
        """
        Ensure the user has all permissions.
        """

        missing = [
            permission for permission in permissions if not user.has_perm(permission)
        ]

        if missing:
            raise permission_denied(
                message=("Missing permissions: " + ", ".join(missing)),
            )


__all__ = ("PermissionService",)
