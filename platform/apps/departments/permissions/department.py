"""
Permission classes for the Departments application.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewDepartment(BasePermission):
    """
    Allows viewing departments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateDepartment(BasePermission):
    """
    Allows creating departments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class CanUpdateDepartment(BasePermission):
    """
    Allows updating departments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class CanDeleteDepartment(BasePermission):
    """
    Allows deleting departments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


__all__ = [
    "CanViewDepartment",
    "CanCreateDepartment",
    "CanUpdateDepartment",
    "CanDeleteDepartment",
]
