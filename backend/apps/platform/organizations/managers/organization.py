"""
Organization manager.
"""

from __future__ import annotations

from apps.core.models import BaseManager
from apps.platform.organizations.querysets import (
    OrganizationQuerySet,
)


class OrganizationManager(
    BaseManager["Organization"],
):
    """
    Custom manager for Organization.
    """

    def get_queryset(
        self,
    ) -> OrganizationQuerySet:
        """
        Return the custom Organization queryset.
        """

        return OrganizationQuerySet(
            model=self.model,
            using=self._db,
            hints=self._hints,
        )

    def active(
        self,
    ) -> OrganizationQuerySet:
        """
        Return active organizations.
        """

        return self.get_queryset().active()

    def verified(
        self,
    ) -> OrganizationQuerySet:
        """
        Return verified organizations.
        """

        return self.get_queryset().verified()

    def by_category(
        self,
        category: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a category.
        """

        return self.get_queryset().by_category(
            category,
        )

    def by_type(
        self,
        organization_type: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a type.
        """

        return self.get_queryset().by_type(
            organization_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a status.
        """

        return self.get_queryset().by_status(
            status,
        )

    def by_size(
        self,
        size: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a size.
        """

        return self.get_queryset().by_size(
            size,
        )

    def for_country(
        self,
        country: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a country.
        """

        return self.get_queryset().for_country(
            country,
        )

    def for_state(
        self,
        state: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a state.
        """

        return self.get_queryset().for_state(
            state,
        )

    def for_city(
        self,
        city: str,
    ) -> OrganizationQuerySet:
        """
        Return organizations for a city.
        """

        return self.get_queryset().for_city(
            city,
        )

    def search(
        self,
        query: str,
    ) -> OrganizationQuerySet:
        """
        Search organizations.
        """

        return self.get_queryset().search(
            query,
        )


__all__ = [
    "OrganizationManager",
]
