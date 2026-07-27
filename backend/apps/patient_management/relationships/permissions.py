"""
Permissions for the Patient Relationships module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewRelationship(BasePermission):
    """Permission to view relationships."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_relationships.view_patientrelationship",
        )


class CanCreateRelationship(BasePermission):
    """Permission to create relationships."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_relationships.add_patientrelationship",
        )


class CanUpdateRelationship(BasePermission):
    """Permission to update relationships."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_relationships.change_patientrelationship",
        )


class CanDeleteRelationship(BasePermission):
    """Permission to delete relationships."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_relationships.delete_patientrelationship",
        )


__all__ = [
    "CanCreateRelationship",
    "CanDeleteRelationship",
    "CanUpdateRelationship",
    "CanViewRelationship",
]
