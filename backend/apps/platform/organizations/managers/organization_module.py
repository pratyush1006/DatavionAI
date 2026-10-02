"""
Organization module manager.

Provides manager entry points for
OrganizationModule query operations.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.querysets.organization_module import (
    OrganizationModuleQuerySet,
)


class OrganizationModuleManager(
    BaseManager,
):
    """
    Manager for OrganizationModule.

    Delegates reusable query operations
    to OrganizationModuleQuerySet.
    """

    def get_queryset(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return the base queryset.
        """

        return OrganizationModuleQuerySet(
            self.model,
            using=self._db,
        )

    def enabled(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return enabled module entitlements.
        """

        return self.get_queryset().enabled()

    def disabled(
        self,
    ) -> OrganizationModuleQuerySet:
        """
        Return disabled module entitlements.
        """

        return self.get_queryset().disabled()

    def for_organization(
        self,
        organization: Any,
    ) -> OrganizationModuleQuerySet:
        """
        Return module entitlements for an organization.
        """

        return self.get_queryset().for_organization(
            organization,
        )

    def by_code(
        self,
        module_code: str,
    ) -> OrganizationModuleQuerySet:
        """
        Filter by module code.
        """

        return self.get_queryset().by_code(
            module_code,
        )


__all__: tuple[str, ...] = ("OrganizationModuleManager",)
