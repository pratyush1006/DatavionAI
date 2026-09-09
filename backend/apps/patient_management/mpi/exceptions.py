"""
Domain exceptions for the Master Patient Index.
"""

from __future__ import annotations


class MPIError(Exception):
    """Base exception for Master Patient Index failures."""


class MPIOrganizationError(MPIError):
    """Raised when organization or tenant boundaries are violated."""


class MPIIdentityError(MPIError):
    """Raised when an identity invariant is violated."""


class MPILifecycleError(MPIError):
    """Raised when an invalid MPI lifecycle operation is requested."""


class MPIMergeError(MPIError):
    """Raised when an MPI merge or reversal is invalid."""


__all__ = (
    "MPIError",
    "MPIIdentityError",
    "MPILifecycleError",
    "MPIMergeError",
    "MPIOrganizationError",
)
