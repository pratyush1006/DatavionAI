"""
Organization module queryset.

Reusable database query scopes for
DatavionOS organization module entitlements.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.core.models import BaseQuerySet

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        OrganizationModule,
    )


class OrganizationModuleQuerySet(
    BaseQuerySet["OrganizationModule"],
):
    """
    Custom queryset for OrganizationModule.

    Provides reusable filtering and
    query optimization helpers.
    """

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def enabled(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return enabled module entitlements.
        """

        return self.filter(
            status=OrganizationModule.Status.ENABLED,
            is_active=True,
        )

    def disabled(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return disabled module entitlements.
        """

        return self.filter(
            status=OrganizationModule.Status.DISABLED,
        )

    def trial(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return trial module entitlements.
        """

        return self.filter(
            status=OrganizationModule.Status.TRIAL,
        )

    def locked(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return locked module entitlements.
        """

        return self.filter(
            status=OrganizationModule.Status.LOCKED,
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationModuleQuerySet:
        """
        Return module entitlements for an organization.
        """

        return self.filter(
            organization=organization,
        )

    # ------------------------------------------------------------------
    # Module
    # ------------------------------------------------------------------

    def by_code(
        self,
        module_code: str,
    ) -> OrganizationModuleQuerySet:
        """
        Filter by module code.
        """

        return self.filter(
            module_code=module_code,
        )

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Load the related organization.
        """

        return self.select_related(
            "organization",
        )


__all__: tuple[str, ...] = ("OrganizationModuleQuerySet",)
