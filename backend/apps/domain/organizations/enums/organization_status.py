"""
Organization status enumeration.
"""

from __future__ import annotations

from enum import StrEnum


class OrganizationStatus(
    StrEnum,
):
    """
    Supported organization lifecycle states.
    """

    PENDING = "pending"

    ACTIVE = "active"

    SUSPENDED = "suspended"

    INACTIVE = "inactive"

    ARCHIVED = "archived"
