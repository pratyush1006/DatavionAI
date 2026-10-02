"""Insurance Verification lifecycle and normalized result constants."""

from __future__ import annotations

from enum import StrEnum


class VerificationStatus(StrEnum):
    """Supported Insurance Verification lifecycle states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"
    INACTIVE = "inactive"


class VerificationOutcome(StrEnum):
    """Normalized verification outcomes."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


class VerificationMethod(StrEnum):
    """Supported verification initiation methods."""

    MANUAL = "manual"
    PAYER_API = "payer_api"
    CLEARINGHOUSE = "clearinghouse"
    IMPORT = "import"


__all__ = ("VerificationMethod", "VerificationOutcome", "VerificationStatus")
