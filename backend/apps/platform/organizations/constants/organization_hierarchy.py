"""
Organization hierarchy constants.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class OrganizationHierarchyRelationshipType(
    StrEnum,
):
    """
    Supported organization hierarchy relationship types.
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

    @classmethod
    def choices(
        cls,
    ) -> tuple[tuple[str, str], ...]:
        """
        Return Django-compatible choices.
        """
        return (
            (cls.HOLDING, "Holding Company"),
            (cls.SUBSIDIARY, "Subsidiary"),
            (cls.BRANCH, "Branch"),
            (cls.DIVISION, "Division"),
            (cls.AFFILIATE, "Affiliate"),
            (cls.FRANCHISE, "Franchise"),
            (cls.PARTNER, "Partner"),
            (cls.NETWORK, "Network"),
            (cls.OTHER, "Other"),
        )


class OrganizationHierarchyStatus(
    StrEnum,
):
    """
    Supported organization hierarchy statuses.
    """

    ACTIVE = "active"

    INACTIVE = "inactive"

    PENDING = "pending"

    ARCHIVED = "archived"

    @classmethod
    def choices(
        cls,
    ) -> tuple[tuple[str, str], ...]:
        """
        Return Django-compatible choices.
        """
        return (
            (cls.ACTIVE, "Active"),
            (cls.INACTIVE, "Inactive"),
            (cls.PENDING, "Pending"),
            (cls.ARCHIVED, "Archived"),
        )


DEFAULT_ORGANIZATION_HIERARCHY_STATUS: Final[str] = OrganizationHierarchyStatus.ACTIVE

DEFAULT_ORGANIZATION_HIERARCHY_RELATIONSHIP_TYPE: Final[str] = (
    OrganizationHierarchyRelationshipType.BRANCH
)


__all__: tuple[str, ...] = (
    "OrganizationHierarchyRelationshipType",
    "OrganizationHierarchyStatus",
    "DEFAULT_ORGANIZATION_HIERARCHY_STATUS",
    "DEFAULT_ORGANIZATION_HIERARCHY_RELATIONSHIP_TYPE",
)
