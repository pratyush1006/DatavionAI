"""
Tenant enumerations for the Datavion AI platform.
"""

from __future__ import annotations

from enum import StrEnum


class TenantStatus(StrEnum):
    """
    Tenant lifecycle status.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class TenantType(StrEnum):
    """
    Supported tenant types.
    """

    CLINIC = "clinic"
    HOSPITAL = "hospital"
    DIAGNOSTIC_CENTER = "diagnostic_center"
    PHARMACY = "pharmacy"
    ORGANIZATION = "organization"


__all__ = [
    "TenantStatus",
    "TenantType",
]
