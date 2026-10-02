"""
Organization feature queryset.

Reusable database query scopes for
DatavionOS organization feature entitlements.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        OrganizationFeature,
    )


class OrganizationFeatureQuerySet(
    BaseQuerySet["OrganizationFeature"],
):
    """
    Custom queryset for OrganizationFeature.

    Provides reusable filtering and
    query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def enabled(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return enabled feature entitlements.
        """

        return self.filter(
            status=OrganizationFeature.Status.ENABLED,
            is_active=True,
        )

    def disabled(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return disabled feature entitlements.
        """

        return self.filter(
            status=OrganizationFeature.Status.DISABLED,
        )

    def trial(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return trial feature entitlements.
        """

        return self.filter(
            status=OrganizationFeature.Status.TRIAL,
        )

    def locked(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Return locked feature entitlements.
        """

        return self.filter(
            status=OrganizationFeature.Status.LOCKED,
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationFeatureQuerySet:
        """
        Return feature entitlements for an organization.
        """

        return self.filter(
            organization=organization,
        )

    # ------------------------------------------------------------------
    # Feature
    # ------------------------------------------------------------------

    def by_code(
        self,
        feature_code: str,
    ) -> OrganizationFeatureQuerySet:
        """
        Filter by feature code.
        """

        return self.filter(
            feature_code=feature_code,
        )

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationFeatureQuerySet:
        """
        Load the related organization.
        """

        return self.select_related(
            "organization",
        )


__all__: tuple[str, ...] = ("OrganizationFeatureQuerySet",)
