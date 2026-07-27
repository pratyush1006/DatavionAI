"""
Permissions for the Master Patient Index module.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewMPI(BasePermission):
    """Permission to view MPI records."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_mpi.view_masterpatientindex",
        )


class CanCreateMPI(BasePermission):
    """Permission to create MPI records."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_mpi.add_masterpatientindex",
        )


class CanUpdateMPI(BasePermission):
    """Permission to update MPI records."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_mpi.change_masterpatientindex",
        )


class CanDeleteMPI(BasePermission):
    """Permission to delete MPI records."""

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.has_perm(
            "patient_mpi.delete_masterpatientindex",
        )


__all__ = [
    "CanCreateMPI",
    "CanDeleteMPI",
    "CanUpdateMPI",
    "CanViewMPI",
]
