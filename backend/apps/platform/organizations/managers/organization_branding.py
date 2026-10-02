"""
Organization branding manager.

Provides manager entry points for
OrganizationBranding query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets import (
    OrganizationBrandingQuerySet,
)


class OrganizationBrandingManager(
    BaseManager,
):
    """
    Manager for OrganizationBranding.

    Delegates reusable query operations
    to OrganizationBrandingQuerySet.
    """

    _queryset_class = OrganizationBrandingQuerySet

    def get_queryset(
        self,
    ) -> OrganizationBrandingQuerySet:
        """
        Return the base queryset.
        """

        return self._queryset_class(
            self.model,
            using=self._db,
        )

    def with_related(
        self,
    ) -> OrganizationBrandingQuerySet:
        """
        Return branding with related organization loaded.
        """

        return self.get_queryset().with_related()

    def by_organization(
        self,
        organization: Any,
    ) -> OrganizationBrandingQuerySet:
        """
        Filter by organization.
        """

        return self.get_queryset().by_organization(
            organization,
        )

    def by_custom_domain(
        self,
        custom_domain: str,
    ) -> OrganizationBrandingQuerySet:
        """
        Filter by custom domain.
        """

        return self.get_queryset().by_custom_domain(
            custom_domain,
        )


__all__: tuple[str, ...] = ("OrganizationBrandingManager",)
