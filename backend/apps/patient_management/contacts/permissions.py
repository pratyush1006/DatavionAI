"""
Permissions for the Contacts module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewContact(BasePermission):
    """Permission to view contacts."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_contacts.view_contact",
        )


class CanCreateContact(BasePermission):
    """Permission to create contacts."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_contacts.add_contact",
        )


class CanUpdateContact(BasePermission):
    """Permission to update contacts."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_contacts.change_contact",
        )


class CanDeleteContact(BasePermission):
    """Permission to delete contacts."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_contacts.delete_contact",
        )


__all__ = [
    "CanCreateContact",
    "CanDeleteContact",
    "CanUpdateContact",
    "CanViewContact",
]
