"""
RBAC adapters for the Master Patient Index.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanListMPI(RBACPermissionBase):
    """Require MPI list permission."""

    permission_code = "patient_mpi.list"
    message = "You do not have permission to list MPI records."


class CanViewMPI(RBACPermissionBase):
    """Require MPI view permission."""

    permission_code = "patient_mpi.view"
    message = "You do not have permission to view MPI records."


class CanCreateMPI(RBACPermissionBase):
    """Require MPI create permission."""

    permission_code = "patient_mpi.create"
    message = "You do not have permission to create MPI records."


class CanUpdateMPI(RBACPermissionBase):
    """Require MPI update permission."""

    permission_code = "patient_mpi.update"
    message = "You do not have permission to update MPI records."


class CanDeleteMPI(RBACPermissionBase):
    """Require MPI delete permission."""

    permission_code = "patient_mpi.delete"
    message = "You do not have permission to delete MPI records."


class CanTransitionMPI(RBACPermissionBase):
    """Require MPI lifecycle transition permission."""

    permission_code = "patient_mpi.transition"
    message = "You do not have permission to change MPI lifecycle state."


class CanMatchMPI(RBACPermissionBase):
    """Require MPI candidate matching permission."""

    permission_code = "patient_mpi.match"
    message = "You do not have permission to generate MPI matches."


class CanReviewMPI(RBACPermissionBase):
    """Require MPI candidate review permission."""

    permission_code = "patient_mpi.review"
    message = "You do not have permission to review MPI matches."


class CanMergeMPI(RBACPermissionBase):
    """Require MPI merge permission."""

    permission_code = "patient_mpi.merge"
    message = "You do not have permission to merge MPI records."


class CanReverseMergeMPI(RBACPermissionBase):
    """Require MPI merge reversal permission."""

    permission_code = "patient_mpi.reverse_merge"
    message = "You do not have permission to reverse MPI merges."


class CanRestoreMPI(RBACPermissionBase):
    """Require MPI restore permission."""

    permission_code = "patient_mpi.restore"
    message = "You do not have permission to restore MPI records."


__all__ = (
    "CanCreateMPI",
    "CanDeleteMPI",
    "CanListMPI",
    "CanMatchMPI",
    "CanMergeMPI",
    "CanReviewMPI",
    "CanRestoreMPI",
    "CanReverseMergeMPI",
    "CanTransitionMPI",
    "CanUpdateMPI",
    "CanViewMPI",
)
