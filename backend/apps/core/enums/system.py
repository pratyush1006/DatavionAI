"""
Tenant enumerations for the DatavionOS platform.

Defines tenant lifecycle and healthcare organization
types used across the multi-tenant SaaS platform.
"""

from __future__ import annotations

from enum import StrEnum


class TenantStatus(StrEnum):
    """
    Tenant lifecycle status.
    """

    PENDING = "pending"

    ONBOARDING = "onboarding"

    TRIAL = "trial"

    ACTIVE = "active"

    INACTIVE = "inactive"

    SUSPENDED = "suspended"

    EXPIRED = "expired"

    CANCELLED = "cancelled"

    ARCHIVED = "archived"


class TenantType(StrEnum):
    """
    Supported healthcare tenant types.
    """

    CLINIC = "clinic"

    HOSPITAL = "hospital"

    DIAGNOSTIC_CENTER = "diagnostic_center"

    LABORATORY = "laboratory"

    PHARMACY = "pharmacy"

    ORGANIZATION = "organization"


__all__ = [
    "TenantStatus",
    "TenantType",
]
