"""
Organization model manager.

Provides the default organization query interface for
DatavionOS.

Lifecycle semantics
-------------------
Organization.objects
    Returns non-soft-deleted, non-archived organizations.

Organization.objects.active()
    Returns operationally active organizations.

Organization.objects.inactive()
    Returns inactive, non-archived organizations.

Organization.objects.archived()
    Returns archived, non-soft-deleted organizations.

Organization.all_objects
    Provided by SoftDeleteModel and includes soft-deleted
    and non-soft-deleted organizations.

Organization.deleted_objects
    Provided by SoftDeleteModel and returns soft-deleted
    organizations only.

Important
---------
Organization archival is a business lifecycle state and is
intentionally separate from soft deletion.

An archived organization therefore has:

    is_deleted = False
    status = OrganizationStatus.ARCHIVED

Such organizations must not appear through the normal
Organization.objects manager.
"""

from __future__ import annotations

from typing import Any

from apps.core.models.managers import BaseManager
from apps.platform.organizations.constants import (
    OrganizationStatus,
)
from apps.platform.organizations.querysets.organization import (
    OrganizationQuerySet,
)


class OrganizationManager(
    BaseManager,
):
    """
    Manager for the Organization model.

    The default organization scope excludes:

        - soft-deleted organizations
        - archived organizations

    Lifecycle-specific scopes are exposed explicitly through
    manager methods.
    """

    def get_queryset(
        self,
    ) -> OrganizationQuerySet:
        """
        Return the default organization queryset.

        Default visibility contract:

            is_deleted = False
            status != ARCHIVED

        This ensures archived organizations do not leak into
        normal organization queries.
        """

        return (
            OrganizationQuerySet(
                self.model,
                using=self._db,
            )
            .filter(
                is_deleted=False,
            )
            .exclude(
                status=OrganizationStatus.ARCHIVED,
            )
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def active(
        self,
    ) -> OrganizationQuerySet:
        """
        Return operationally active organizations.

        Requires:

            is_deleted = False
            status = ACTIVE
            is_active = True
        """

        return self.get_queryset().active()

    def inactive(
        self,
    ) -> OrganizationQuerySet:
        """
        Return inactive, non-archived organizations.
        """

        return self.get_queryset().inactive()

    def archived(
        self,
    ) -> OrganizationQuerySet:
        """
        Return non-soft-deleted archived organizations.

        Because get_queryset() intentionally excludes archived
        organizations, this method must start from a queryset
        that explicitly restores the archived scope.

        The implementation therefore queries directly through
        the model's base queryset rather than the normal
        organization visibility scope.
        """

        return OrganizationQuerySet(
            self.model,
            using=self._db,
        ).filter(
            is_deleted=False,
            status=OrganizationStatus.ARCHIVED,
        )

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
        Return non-archived organizations belonging to
        the specified tenant.
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
        Return non-archived organizations by category.
        """

        return self.get_queryset().by_category(
            category,
        )

    def by_type(
        self,
        organization_type: str,
    ) -> OrganizationQuerySet:
        """
        Return non-archived organizations by organization type.
        """

        return self.get_queryset().by_type(
            organization_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationQuerySet:
        """
        Return non-archived organizations by lifecycle status.

        Note:
            Use archived() explicitly when querying archived
            organizations.
        """

        return self.get_queryset().by_status(
            status,
        )

    def by_size(
        self,
        size: str,
    ) -> OrganizationQuerySet:
        """
        Return non-archived organizations by size.
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
        Return non-archived production organizations.
        """

        return self.get_queryset().production()

    def demo(
        self,
    ) -> OrganizationQuerySet:
        """
        Return non-archived demo organizations.
        """

        return self.get_queryset().demo()

    # ------------------------------------------------------------------
    # Query Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationQuerySet:
        """
        Return non-archived organizations with commonly
        accessed related objects preloaded.
        """

        return self.get_queryset().with_related()

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> OrganizationQuerySet:
        """
        Search non-archived organizations.
        """

        return self.get_queryset().search(
            query,
        )


__all__: tuple[str, ...] = ("OrganizationManager",)
