"""Prior Authorization lifecycle and normalized authorization constants."""

from __future__ import annotations

from enum import StrEnum


class AuthorizationStatus(StrEnum):
    """Supported Prior Authorization lifecycle states."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    INACTIVE = "inactive"


class AuthorizationOutcome(StrEnum):
    """Normalized authorization outcomes."""

    APPROVED = "approved"
    DENIED = "denied"
    PENDED = "pended"
    NOT_REQUIRED = "not_required"
    UNKNOWN = "unknown"


class AuthorizationMethod(StrEnum):
    """Supported authorization submission methods."""

    MANUAL = "manual"
    PAYER_API = "payer_api"
    CLEARINGHOUSE = "clearinghouse"
    PORTAL = "portal"
    IMPORT = "import"


__all__ = ("AuthorizationMethod", "AuthorizationOutcome", "AuthorizationStatus")
