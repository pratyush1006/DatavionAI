"""
Permission-related API mixins.
"""

from __future__ import annotations

from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission


class PermissionMapMixin:
    """
    Map HTTP methods to permission classes.
    """

    permission_map: dict[
        str,
        tuple[type[BasePermission], ...],
    ] = {}

    def get_permission_classes(
        self,
    ) -> tuple[type[BasePermission], ...]:
        """
        Return configured permission classes.
        """

        permission_classes = self.permission_map.get(
            self.request.method,
        )

        if permission_classes is None:
            raise ImproperlyConfigured(
                f"No permission_map configured for {self.request.method}."
            )

        return permission_classes

    def get_permissions(
        self,
    ) -> list[BasePermission]:
        """
        Instantiate permission classes.
        """

        return [permission() for permission in self.get_permission_classes()]


__all__ = [
    "PermissionMapMixin",
]
