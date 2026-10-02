"""
Tenant managers and querysets.

Provides reusable tenant database operations.
"""

from __future__ import annotations

from django.db import models

from apps.platform.tenancy.constants import (
    TenantStatus,
)


class TenantQuerySet(
    models.QuerySet,
):
    """
    QuerySet for Tenant operations.
    """

    def active(
        self,
    ):
        """
        Return active tenants.
        """

        return self.filter(
            status=TenantStatus.ACTIVE,
        )

    def available(
        self,
    ):
        """
        Return tenants available for usage.
        """

        return self.filter(
            status=TenantStatus.ACTIVE,
        )

    def by_slug(
        self,
        slug: str,
    ):
        """
        Find tenant by slug.
        """

        return self.filter(
            slug=slug,
        )


class TenantManager(
    models.Manager.from_queryset(
        TenantQuerySet,
    ),
):
    """
    Default tenant manager.
    """


__all__ = (
    "TenantManager",
    "TenantQuerySet",
)
