"""
Organization membership queryset.

Reusable database filters for
organization membership management.
"""

from __future__ import annotations

from apps.core.models import BaseQuerySet


class OrganizationMembershipQuerySet(
    BaseQuerySet["OrganizationMembership"],
):
    """
    QuerySet for organization memberships.

    Provides reusable membership
    lifecycle and ownership filters.
    """

    def active(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return active memberships.
        """

        return self.filter(
            status="active",
        )

    def invited(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return invited memberships.
        """

        return self.filter(
            status="invited",
        )

    def suspended(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return suspended memberships.
        """

        return self.filter(
            status="suspended",
        )

    def removed(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return removed memberships.
        """

        return self.filter(
            status="removed",
        )

    def for_organization(
        self,
        organization_id,
    ) -> OrganizationMembershipQuerySet:
        """
        Filter memberships by organization.
        """

        return self.filter(
            organization_id=organization_id,
        )

    def for_user(
        self,
        user_id,
    ) -> OrganizationMembershipQuerySet:
        """
        Filter memberships by user.
        """

        return self.filter(
            user_id=user_id,
        )

    def primary(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return primary organization memberships.
        """

        return self.filter(
            is_primary=True,
        )

    def with_related(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Optimize common membership access.
        """

        return self.select_related(
            "organization",
            "user",
        )


__all__ = [
    "OrganizationMembershipQuerySet",
]
