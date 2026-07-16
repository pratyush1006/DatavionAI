"""
Organization queryset.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseQuerySet


class OrganizationQuerySet(
    BaseQuerySet["Organization"],
):
    """
    Custom queryset for Organization.
    """

    def active(
        self,
    ) -> OrganizationQuerySet:
        """
        Return active organizations.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> OrganizationQuerySet:
        """
        Return inactive organizations.
        """

        return self.filter(
            is_active=False,
        )

    def verified(
        self,
    ) -> OrganizationQuerySet:
        """
        Return verified organizations.
        """

        return self.filter(
            is_verified=True,
        )

    def by_category(
        self,
        category: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization category.
        """

        return self.filter(
            category=category,
        )

    def by_type(
        self,
        organization_type: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization type.
        """

        return self.filter(
            organization_type=organization_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization status.
        """

        return self.filter(
            status=status,
        )

    def by_size(
        self,
        size: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization size.
        """

        return self.filter(
            size=size,
        )

    def for_country(
        self,
        country: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by country.
        """

        return self.filter(
            country=country,
        )

    def for_state(
        self,
        state: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by state.
        """

        return self.filter(
            state=state,
        )

    def for_city(
        self,
        city: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by city.
        """

        return self.filter(
            city=city,
        )

    def with_related(
        self,
    ) -> OrganizationQuerySet:
        """
        Load commonly accessed related objects.
        """

        return self.select_related()

    def search(
        self,
        query: str,
    ) -> OrganizationQuerySet:
        """
        Search organizations.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                name__icontains=query,
            )
            | models.Q(
                display_name__icontains=query,
            )
            | models.Q(
                code__icontains=query,
            )
            | models.Q(
                email__icontains=query,
            )
        ).distinct()


__all__ = [
    "OrganizationQuerySet",
]
