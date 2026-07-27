"""
Permissions for the Patient Preferences module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewPatientPreference(BasePermission):
    """
    Permission to view patient preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.view_patientpreference",
        )


class CanCreatePatientPreference(BasePermission):
    """
    Permission to create patient preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.add_patientpreference",
        )


class CanUpdatePatientPreference(BasePermission):
    """
    Permission to update patient preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.change_patientpreference",
        )


class CanDeletePatientPreference(BasePermission):
    """
    Permission to delete patient preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.delete_patientpreference",
        )


class CanViewCommunicationPreference(BasePermission):
    """
    Permission to view communication preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.view_patientcommunicationpreference",
        )


class CanCreateCommunicationPreference(BasePermission):
    """
    Permission to create communication preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.add_patientcommunicationpreference",
        )


class CanUpdateCommunicationPreference(BasePermission):
    """
    Permission to update communication preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.change_patientcommunicationpreference",
        )


class CanDeleteCommunicationPreference(BasePermission):
    """
    Permission to delete communication preferences.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "preferences.delete_patientcommunicationpreference",
        )


__all__ = [
    "CanCreateCommunicationPreference",
    "CanCreatePatientPreference",
    "CanDeleteCommunicationPreference",
    "CanDeletePatientPreference",
    "CanUpdateCommunicationPreference",
    "CanUpdatePatientPreference",
    "CanViewCommunicationPreference",
    "CanViewPatientPreference",
]
