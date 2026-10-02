"""
Serializer field definitions for the Organization Domain API.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------
# List Serializer
# ---------------------------------------------------------------------

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "domain",
    "domain_type",
    "is_primary",
    "verification_status",
    "ssl_enabled",
    "verified_at",
)

# ---------------------------------------------------------------------
# Detail Serializer
# ---------------------------------------------------------------------

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "domain",
    "domain_type",
    "is_primary",
    "verification_status",
    "verification_token_hash",
    "verified_at",
    "ssl_enabled",
    "ssl_expiry_date",
    "created_at",
    "updated_at",
)

# ---------------------------------------------------------------------
# Create Serializer
# ---------------------------------------------------------------------

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "domain",
    "domain_type",
    "is_primary",
)

# ---------------------------------------------------------------------
# Update Serializer
# ---------------------------------------------------------------------

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "domain",
    "domain_type",
    "is_primary",
)

__all__ = [
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
]
