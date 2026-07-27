"""
Organization manager.

Provides manager entry points for the
DatavionOS Organizations bounded context.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets.organization import (
    OrganizationQuerySet,
)


class OrganizationManager(
    BaseManager,
):
    """
    Manager for the Organization model.

    Exposes reusable query helpers by
    delegating to OrganizationQuerySet.
    """

    def get_queryset(
        self,
    ) -> OrganizationQuerySet:
        """
        Return the base organization queryset.
        """

        return OrganizationQuerySet(
            self.model,
            using=self._db,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def active(
        self,
    ) -> OrganizationQuerySet:
        """
        Return active organizations.
        """

        return self.get_queryset().active()

    def inactive(
        self,
    ) -> OrganizationQuerySet:
        """
        Return inactive organizations.
        """

        return self.get_queryset().inactive()

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verified(
        self,
    ) -> OrganizationQuerySet:
        """
        Return verified organizations.
        """

        return self.get_queryset().verified()

    def unverified(
        self,
    ) -> OrganizationQuerySet:
        """
        Return unverified organizations.
        """

        return self.get_queryset().unverified()

    def pending_verification(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations awaiting verification.
        """

        return self.get_queryset().pending_verification()

    # ------------------------------------------------------------------
    # Tenant
    # ------------------------------------------------------------------

    def for_tenant(
        self,
        tenant: Any,
    ) -> OrganizationQuerySet:
        """
        Return organizations for the given tenant.
        """

        return self.get_queryset().for_tenant(
            tenant,
        )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def by_category(
        self,
        category: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by category.
        """

        return self.get_queryset().by_category(
            category,
        )

    def by_type(
        self,
        organization_type: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by type.
        """

        return self.get_queryset().by_type(
            organization_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by status.
        """

        return self.get_queryset().by_status(
            status,
        )

    def by_size(
        self,
        size: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by size.
        """

        return self.get_queryset().by_size(
            size,
        )

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    def production(
        self,
    ) -> OrganizationQuerySet:
        """
        Return production organizations.
        """

        return self.get_queryset().production()

    def demo(
        self,
    ) -> OrganizationQuerySet:
        """
        Return demo organizations.
        """

        return self.get_queryset().demo()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

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


__all__: tuple[str, ...] = ("OrganizationManager",)
