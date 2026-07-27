"""
Serializer field definitions for OrganizationSettings.
"""

from __future__ import annotations

from typing import Final

# ==========================================================
# List Serializer
# ==========================================================

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "language",
    "timezone",
    "currency",
    "mfa_required",
)

# ==========================================================
# Detail Serializer
# ==========================================================

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "language",
    "timezone",
    "currency",
    "date_format",
    "time_format",
    "email_notifications",
    "sms_notifications",
    "push_notifications",
    "session_timeout_minutes",
    "mfa_required",
    "default_dashboard",
    "created_at",
    "updated_at",
)

# ==========================================================
# Create Serializer
# ==========================================================

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "language",
    "timezone",
    "currency",
    "date_format",
    "time_format",
    "email_notifications",
    "sms_notifications",
    "push_notifications",
    "session_timeout_minutes",
    "mfa_required",
    "default_dashboard",
)

# ==========================================================
# Update Serializer
# ==========================================================

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "language",
    "timezone",
    "currency",
    "date_format",
    "time_format",
    "email_notifications",
    "sms_notifications",
    "push_notifications",
    "session_timeout_minutes",
    "mfa_required",
    "default_dashboard",
)

__all__: tuple[str, ...] = (
    "_DETAIL_FIELDS",
    "_LIST_FIELDS",
    "_UPDATE_FIELDS",
    "_WRITE_FIELDS",
)
