"""
Organization membership manager.

Provides reusable query entry points
for organization user memberships.
"""

from __future__ import annotations

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets.organization_membership import (
    OrganizationMembershipQuerySet,
)


class OrganizationMembershipManager(
    BaseManager,
):
    """
    Manager for OrganizationMembership.

    Handles organization membership
    lifecycle queries.
    """

    def get_queryset(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return membership queryset.
        """

        return OrganizationMembershipQuerySet(
            self.model,
            using=self._db,
        )

    def active(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return active memberships.
        """

        return self.get_queryset().active()

    def invited(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return invited memberships.
        """

        return self.get_queryset().invited()

    def suspended(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return suspended memberships.
        """

        return self.get_queryset().suspended()

    def removed(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return removed memberships.
        """

        return self.get_queryset().removed()

    def for_organization(
        self,
        organization_id,
    ) -> OrganizationMembershipQuerySet:
        """
        Return memberships for organization.
        """

        return self.get_queryset().for_organization(
            organization_id,
        )

    def for_user(
        self,
        user_id,
    ) -> OrganizationMembershipQuerySet:
        """
        Return memberships for user.
        """

        return self.get_queryset().for_user(
            user_id,
        )

    def primary(
        self,
    ) -> OrganizationMembershipQuerySet:
        """
        Return primary organization memberships.
        """

        return self.get_queryset().primary()


__all__ = [
    "OrganizationMembershipManager",
]
