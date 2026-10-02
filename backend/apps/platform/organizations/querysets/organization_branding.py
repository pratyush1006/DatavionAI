"""
Organization branding queryset.

Reusable database query scopes for
DatavionOS organization branding.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    pass


class OrganizationBrandingQuerySet(
    BaseQuerySet["OrganizationBranding"],
):
    """
    Custom queryset for OrganizationBranding.

    Provides reusable filtering and
    query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationBrandingQuerySet:
        """
        Load the related organization.
        """

        return self.select_related(
            "organization",
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def by_organization(
        self,
        organization: Any,
    ) -> OrganizationBrandingQuerySet:
        """
        Filter branding by organization.
        """

        return self.filter(
            organization=organization,
        )

    # ------------------------------------------------------------------
    # Domain
    # ------------------------------------------------------------------

    def by_custom_domain(
        self,
        custom_domain: str,
    ) -> OrganizationBrandingQuerySet:
        """
        Filter by custom domain.
        """

        return self.filter(
            custom_domain=custom_domain.strip().lower(),
        )


__all__: tuple[str, ...] = ("OrganizationBrandingQuerySet",)
