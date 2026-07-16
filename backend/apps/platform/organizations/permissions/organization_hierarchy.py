"""
Permissions for the Organization Hierarchy application.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewOrganizationHierarchy(
    BasePermission,
):
    """
    Permission to view organization hierarchies.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can view organization hierarchies.
        """

        return request.user.is_authenticated


class CanCreateOrganizationHierarchy(
    BasePermission,
):
    """
    Permission to create organization hierarchies.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can create organization hierarchies.
        """

        return request.user.is_authenticated


class CanUpdateOrganizationHierarchy(
    BasePermission,
):
    """
    Permission to update organization hierarchies.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can update organization hierarchies.
        """

        return request.user.is_authenticated


class CanDeleteOrganizationHierarchy(
    BasePermission,
):
    """
    Permission to delete organization hierarchies.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can delete organization hierarchies.
        """

        return request.user.is_authenticated


__all__ = [
    "CanViewOrganizationHierarchy",
    "CanCreateOrganizationHierarchy",
    "CanUpdateOrganizationHierarchy",
    "CanDeleteOrganizationHierarchy",
]
