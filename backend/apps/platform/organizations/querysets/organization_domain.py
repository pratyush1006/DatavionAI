"""
Organization domain queryset.

Reusable database query scopes for
DatavionOS organization domains.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    pass


class OrganizationDomainQuerySet(
    BaseQuerySet["OrganizationDomain"],
):
    """
    Custom queryset for OrganizationDomain.

    Provides reusable filtering, searching
    and query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def by_organization(
        self,
        organization: Any,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains belonging to an organization.
        """

        return self.filter(
            organization=organization,
        )

    # ------------------------------------------------------------------
    # Domain type
    # ------------------------------------------------------------------

    def by_type(
        self,
        domain_type: str,
    ) -> OrganizationDomainQuerySet:
        """
        Filter domains by domain type.
        """

        return self.filter(
            domain_type=domain_type,
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

        return self.filter(
            is_primary=True,
        )

    def non_primary(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return non-primary domains.
        """

        return self.filter(
            is_primary=False,
        )

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verified(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return verified domains.
        """

        from apps.platform.organizations.models import (
            OrganizationDomain,
        )

        return self.filter(
            verification_status=(OrganizationDomain.VerificationStatus.VERIFIED),
        )

    def pending_verification(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains awaiting verification.
        """

        from apps.platform.organizations.models import (
            OrganizationDomain,
        )

        return self.filter(
            verification_status=(OrganizationDomain.VerificationStatus.PENDING),
        )

    def failed_verification(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains whose verification failed.
        """

        from apps.platform.organizations.models import (
            OrganizationDomain,
        )

        return self.filter(
            verification_status=(OrganizationDomain.VerificationStatus.FAILED),
        )

    # ------------------------------------------------------------------
    # SSL
    # ------------------------------------------------------------------

    def ssl_enabled(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains with SSL enabled.
        """

        return self.filter(
            ssl_enabled=True,
        )

    def ssl_disabled(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Return domains without SSL enabled.
        """

        return self.filter(
            ssl_enabled=False,
        )

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationDomainQuerySet:
        """
        Load the related organization.
        """

        return self.select_related(
            "organization",
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> OrganizationDomainQuerySet:
        """
        Search domains by hostname.
        """

        query = query.strip().lower()

        if not query:
            return self

        return self.filter(
            domain__icontains=query,
        )


__all__: tuple[str, ...] = ("OrganizationDomainQuerySet",)
