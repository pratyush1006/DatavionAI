"""
Organization profile queryset.

Reusable database query scopes for
DatavionOS organization profiles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    pass


class OrganizationProfileQuerySet(
    BaseQuerySet["OrganizationProfile"],
):
    """
    Custom queryset for OrganizationProfile.

    Provides reusable filtering and
    query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationProfileQuerySet:
        """
        Return the profile for an organization.
        """

        return self.filter(
            organization=organization,
        )

    # ------------------------------------------------------------------
    # Healthcare
    # ------------------------------------------------------------------

    def healthcare(
        self,
    ) -> OrganizationProfileQuerySet:
        """
        Return healthcare organizations.
        """

        return self.filter(
            industry="healthcare",
        )

    def by_facility_type(
        self,
        facility_type: str,
    ) -> OrganizationProfileQuerySet:
        """
        Filter by healthcare facility type.
        """

        return self.filter(
            facility_type=facility_type,
        )

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationProfileQuerySet:
        """
        Load related organization.
        """

        return self.select_related(
            "organization",
        )


__all__: tuple[str, ...] = ("OrganizationProfileQuerySet",)
