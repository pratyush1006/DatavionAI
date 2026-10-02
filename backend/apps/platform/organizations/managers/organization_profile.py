"""
Organization profile manager.

Provides manager entry points for
OrganizationProfile query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets.organization_profile import (
    OrganizationProfileQuerySet,
)


class OrganizationProfileManager(
    BaseManager,
):
    """
    Manager for OrganizationProfile.

    Delegates reusable query operations
    to OrganizationProfileQuerySet.
    """

    def get_queryset(
        self,
    ) -> OrganizationProfileQuerySet:
        """
        Return the base queryset.
        """

        return OrganizationProfileQuerySet(
            self.model,
            using=self._db,
        )

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationProfileQuerySet:
        """
        Return the profile for an organization.
        """

        return self.get_queryset().for_organization(
            organization,
        )

    def healthcare(
        self,
    ) -> OrganizationProfileQuerySet:
        """
        Return healthcare organizations.
        """

        return self.get_queryset().healthcare()

    def by_facility_type(
        self,
        facility_type: str,
    ) -> OrganizationProfileQuerySet:
        """
        Filter by facility type.
        """

        return self.get_queryset().by_facility_type(
            facility_type,
        )


__all__: tuple[str, ...] = ("OrganizationProfileManager",)
