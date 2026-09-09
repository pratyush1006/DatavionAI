"""
Organization domain manager.

Provides manager entry points for
OrganizationDomain query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import (
    BaseManager,
)
from apps.platform.organizations.querysets.organization_domain import (
    OrganizationDomainQuerySet,
)


class OrganizationDomainManager(
    BaseManager,
):
    """
    Manager for OrganizationDomain.

    Delegates reusable query operations
    to OrganizationDomainQuerySet.
    """

    def get_queryset(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return the base domain queryset.
        """

        return OrganizationDomainQuerySet(
            self.model,
            using=self._db,
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def by_organization(
        self,
        organization: Any,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains for an organization.
        """

        return self.get_queryset().by_organization(
            organization,
        )

    # ------------------------------------------------------------------
    # Domain type
    # ------------------------------------------------------------------

    def by_type(
        self,
        domain_type: str,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains by domain type.
        """

        return self.get_queryset().by_type(
            domain_type,
        )

    # ------------------------------------------------------------------
    # Primary
    # ------------------------------------------------------------------

    def primary(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return primary domains.
        """

        return self.get_queryset().primary()

    def non_primary(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return non-primary domains.
        """

        return self.get_queryset().non_primary()

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verified(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return verified domains.
        """

        return self.get_queryset().verified()

    def pending_verification(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains awaiting verification.
        """

        return self.get_queryset().pending_verification()

    def failed_verification(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains with failed verification.
        """

        return self.get_queryset().failed_verification()

    # ------------------------------------------------------------------
    # SSL
    # ------------------------------------------------------------------

    def ssl_enabled(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains with SSL enabled.
        """

        return self.get_queryset().ssl_enabled()

    def ssl_disabled(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains without SSL enabled.
        """

        return self.get_queryset().ssl_disabled()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> OrganizationDomainQuerySet:
        """
        Search organization domains.
        """

        return self.get_queryset().search(
            query,
        )


__all__: tuple[str, ...] = ("OrganizationDomainManager",)
