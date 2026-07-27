"""
Provider permissions.
"""

from __future__ import annotations

from apps.common.permissions import BasePermission


class ProviderPermission:
    """
    Provider permission codes.
    """

    VIEW = "provider.view"

    CREATE = "provider.create"

    UPDATE = "provider.update"

    DELETE = "provider.delete"


class CanViewProvider(BasePermission):
    """
    Permission to view providers.
    """

    permission_code = ProviderPermission.VIEW


class CanCreateProvider(BasePermission):
    """
    Permission to create providers.
    """

    permission_code = ProviderPermission.CREATE


class CanUpdateProvider(BasePermission):
    """
    Permission to update providers.
    """

    permission_code = ProviderPermission.UPDATE


class CanDeleteProvider(BasePermission):
    """
    Permission to delete providers.
    """

    permission_code = ProviderPermission.DELETE


__all__ = [
    "ProviderPermission",
    "CanViewProvider",
    "CanCreateProvider",
    "CanUpdateProvider",
    "CanDeleteProvider",
]
