"""
Serializer field definitions for the Organization Feature API.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------
# List Serializer
# ---------------------------------------------------------------------

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "feature_code",
    "status",
    "enabled_at",
)

# ---------------------------------------------------------------------
# Detail Serializer
# ---------------------------------------------------------------------

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "feature_code",
    "status",
    "settings",
    "enabled_at",
    "disabled_at",
    "created_at",
    "updated_at",
)

# ---------------------------------------------------------------------
# Create Serializer
# ---------------------------------------------------------------------

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "feature_code",
    "status",
    "settings",
)

# ---------------------------------------------------------------------
# Update Serializer
# ---------------------------------------------------------------------

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "status",
    "settings",
)

__all__ = (
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
)
