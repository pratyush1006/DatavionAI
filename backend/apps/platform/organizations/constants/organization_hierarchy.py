"""
Constants for Organization Hierarchy.
"""

from __future__ import annotations

from typing import Final


class OrganizationHierarchyRelationshipType:
    """
    Organization hierarchy relationship types.
    """

    HOLDING = "holding"

    SUBSIDIARY = "subsidiary"

    BRANCH = "branch"

    DIVISION = "division"

    AFFILIATE = "affiliate"

    FRANCHISE = "franchise"

    PARTNER = "partner"

    NETWORK = "network"

    OTHER = "other"

    CHOICES: Final = (
        (HOLDING, "Holding Company"),
        (SUBSIDIARY, "Subsidiary"),
        (BRANCH, "Branch"),
        (DIVISION, "Division"),
        (AFFILIATE, "Affiliate"),
        (FRANCHISE, "Franchise"),
        (PARTNER, "Partner"),
        (NETWORK, "Network"),
        (OTHER, "Other"),
    )


class OrganizationHierarchyStatus:
    """
    Organization hierarchy status.
    """

    ACTIVE = "active"

    INACTIVE = "inactive"

    PENDING = "pending"

    ARCHIVED = "archived"

    CHOICES: Final = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
        (PENDING, "Pending"),
        (ARCHIVED, "Archived"),
    )


__all__ = [
    "OrganizationHierarchyRelationshipType",
    "OrganizationHierarchyStatus",
]
