"""
Custom exceptions for the Patient Relationships module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class RelationshipError(DatavionException):
    """Base exception for relationship errors."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Patient relationship operation failed."


class DuplicateRelationshipError(RelationshipError):
    """Raised when a duplicate relationship exists."""

    default_detail = "A relationship with the same details already exists."


class InvalidRelationshipError(RelationshipError):
    """Raised when a relationship is invalid."""

    default_detail = "The relationship is invalid."


class RelationshipVerificationError(RelationshipError):
    """Raised when relationship verification fails."""

    default_detail = "Relationship verification failed."


class RelationshipTerminationError(RelationshipError):
    """Raised when a relationship cannot be terminated."""

    default_detail = "Relationship termination failed."


__all__ = [
    "DuplicateRelationshipError",
    "InvalidRelationshipError",
    "RelationshipError",
    "RelationshipTerminationError",
    "RelationshipVerificationError",
]
