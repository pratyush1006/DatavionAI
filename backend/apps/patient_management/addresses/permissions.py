"""
Permissions for the Addresses module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewAddress(BasePermission):
    """Permission to view addresses."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_addresses.view_address",
        )


class CanCreateAddress(BasePermission):
    """Permission to create addresses."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_addresses.add_address",
        )


class CanUpdateAddress(BasePermission):
    """Permission to update addresses."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_addresses.change_address",
        )


class CanDeleteAddress(BasePermission):
    """Permission to delete addresses."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_addresses.delete_address",
        )


__all__ = [
    "CanCreateAddress",
    "CanDeleteAddress",
    "CanUpdateAddress",
    "CanViewAddress",
]
