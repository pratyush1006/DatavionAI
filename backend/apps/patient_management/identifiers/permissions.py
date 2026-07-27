# apps/patient_management/identifiers/permissions.py

"""
Permissions for the Identifiers module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewPatientIdentifier(BasePermission):
    """Permission to view patient identifiers."""

    message = "You do not have permission to view patient identifiers."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "identifiers.view_patientidentifier",
        )


class CanCreatePatientIdentifier(BasePermission):
    """Permission to create patient identifiers."""

    message = "You do not have permission to create patient identifiers."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "identifiers.add_patientidentifier",
        )


class CanUpdatePatientIdentifier(BasePermission):
    """Permission to update patient identifiers."""

    message = "You do not have permission to update patient identifiers."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "identifiers.change_patientidentifier",
        )


class CanDeletePatientIdentifier(BasePermission):
    """Permission to delete patient identifiers."""

    message = "You do not have permission to delete patient identifiers."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "identifiers.delete_patientidentifier",
        )


class CanVerifyPatientIdentifier(BasePermission):
    """Permission to verify patient identifiers."""

    message = "You do not have permission to verify patient identifiers."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "identifiers.verify_patientidentifier",
        )


__all__ = [
    "CanCreatePatientIdentifier",
    "CanDeletePatientIdentifier",
    "CanUpdatePatientIdentifier",
    "CanVerifyPatientIdentifier",
    "CanViewPatientIdentifier",
]
