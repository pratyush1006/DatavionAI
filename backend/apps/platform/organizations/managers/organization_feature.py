"""
Organization feature manager.

Provides manager entry points for
OrganizationFeature query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets.organization_feature import (
    OrganizationFeatureQuerySet,
)


class OrganizationFeatureManager(
    BaseManager,
):
    """
    Manager for OrganizationFeature.

    Delegates reusable query operations
    to OrganizationFeatureQuerySet.
    """

    def get_queryset(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return the base queryset.
        """

        return OrganizationFeatureQuerySet(
            self.model,
            using=self._db,
        )

    def enabled(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return enabled feature entitlements.
        """

        return self.get_queryset().enabled()

    def disabled(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return disabled feature entitlements.
        """

        return self.get_queryset().disabled()

    def trial(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return trial feature entitlements.
        """

        return self.get_queryset().trial()

    def locked(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return locked feature entitlements.
        """

        return self.get_queryset().locked()

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationFeatureQuerySet:
        """
        Return features for an organization.
        """

        return self.get_queryset().for_organization(
            organization,
        )

    def by_code(
        self,
        feature_code: str,
    ) -> OrganizationFeatureQuerySet:
        """
        Filter by feature code.
        """

        return self.get_queryset().by_code(
            feature_code,
        )


__all__: tuple[str, ...] = ("OrganizationFeatureManager",)
