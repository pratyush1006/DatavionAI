"""
Custom exceptions for the Master Patient Index module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class MPIError(DatavionException):
    """Base exception for MPI errors."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Master Patient Index operation failed."


class DuplicateMPIRecordError(MPIError):
    """Raised when a duplicate MPI record exists."""

    default_detail = "A Master Patient Index record already exists."


class MPINotFoundError(MPIError):
    """Raised when an MPI record cannot be found."""

    default_code = ErrorCode.NOT_FOUND
    default_detail = "Master Patient Index record not found."


class MPIMergeError(MPIError):
    """Raised when an MPI merge operation fails."""

    default_detail = "Unable to merge Master Patient Index records."


class MPIVerificationError(MPIError):
    """Raised when verification fails."""

    default_detail = "Master Patient Index verification failed."


__all__ = [
    "DuplicateMPIRecordError",
    "MPIError",
    "MPIMergeError",
    "MPINotFoundError",
    "MPIVerificationError",
]
