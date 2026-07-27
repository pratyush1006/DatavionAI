"""
Identifier type aliases for the Datavion AI platform.

Provides strongly typed UUID identifiers used across
the DatavionOS enterprise SaaS platform.

These types improve readability, static analysis,
and domain separation while keeping UUID as the
underlying storage representation.
"""

from __future__ import annotations

from typing import NewType
from uuid import UUID

# ============================================================================
# Generic Identifiers
# ============================================================================

Identifier = NewType(
    "Identifier",
    UUID,
)

ResourceID = NewType(
    "ResourceID",
    UUID,
)


# ============================================================================
# Multi-Tenant Platform Identifiers
# ============================================================================

TenantID = NewType(
    "TenantID",
    UUID,
)

OrganizationID = NewType(
    "OrganizationID",
    UUID,
)

BranchID = NewType(
    "BranchID",
    UUID,
)


# ============================================================================
# Identity & Access Management Identifiers
# ============================================================================

UserID = NewType(
    "UserID",
    UUID,
)

RoleID = NewType(
    "RoleID",
    UUID,
)

PermissionID = NewType(
    "PermissionID",
    UUID,
)


# ============================================================================
# Healthcare Domain Identifiers
# ============================================================================

PatientID = NewType(
    "PatientID",
    UUID,
)

DepartmentID = NewType(
    "DepartmentID",
    UUID,
)

FacilityID = NewType(
    "FacilityID",
    UUID,
)


# ============================================================================
# Platform Commerce Identifiers
# ============================================================================

SubscriptionID = NewType(
    "SubscriptionID",
    UUID,
)


__all__ = [
    "BranchID",
    "DepartmentID",
    "FacilityID",
    "Identifier",
    "OrganizationID",
    "PatientID",
    "PermissionID",
    "ResourceID",
    "RoleID",
    "SubscriptionID",
    "TenantID",
    "UserID",
]
