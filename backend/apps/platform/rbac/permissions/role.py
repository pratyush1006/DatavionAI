"""
Role API permissions.
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView


class CanViewRole(
    BasePermission,
):
    """
    Permission required to view roles.
    """

    message = "You do not have permission to view roles."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request has permission.
        """

        return request.user.is_authenticated


class CanCreateRole(
    BasePermission,
):
    """
    Permission required to create roles.
    """

    message = "You do not have permission to create roles."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request has permission.
        """

        return request.user.is_authenticated


class CanUpdateRole(
    BasePermission,
):
    """
    Permission required to update roles.
    """

    message = "You do not have permission to update roles."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request has permission.
        """

        return request.user.is_authenticated


class CanDeleteRole(
    BasePermission,
):
    """
    Permission required to delete roles.
    """

    message = "You do not have permission to delete roles."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request has permission.
        """

        return request.user.is_authenticated


__all__ = [
    "CanCreateRole",
    "CanDeleteRole",
    "CanUpdateRole",
    "CanViewRole",
]
