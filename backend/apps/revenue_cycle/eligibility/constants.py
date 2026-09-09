"""Eligibility lifecycle and coverage constants."""

from __future__ import annotations

from enum import StrEnum


class EligibilityStatus(StrEnum):
    """Supported eligibility lifecycle states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    INACTIVE = "inactive"


class CoverageStatus(StrEnum):
    """Normalized coverage outcomes."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    UNKNOWN = "unknown"
    NOT_FOUND = "not_found"


__all__ = ("CoverageStatus", "EligibilityStatus")
