"""
Organization queryset.

Reusable database query scopes for
DatavionOS organization management.

The queryset is intentionally responsible only
for database-level filtering and optimization.

Lifecycle semantics:

    active
        is_active=True AND status=ACTIVE

    inactive
        is_active=False AND status!=ARCHIVED

    archived
        is_deleted=False AND status=ARCHIVED

Soft deletion remains independent from organization
archival:

    is_deleted=True
        The record has been soft-deleted.

    status=ARCHIVED
        The organization has been archived as a
        business lifecycle state.

This distinction is important for auditability,
recovery and enterprise lifecycle management.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseQuerySet
from apps.platform.organizations.constants import (
    OrganizationStatus,
    VerificationStatus,
)


class OrganizationQuerySet(
    BaseQuerySet["Organization"],
):
    """
    Custom queryset for Organization.

    Provides reusable filtering,
    searching and optimization
    helpers for organization data.
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def active(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations that are operationally active.

        Archived organizations must never be returned
        by the active scope, even if their is_active flag
        was not changed during archival.
        """

        return self.filter(
            is_active=True,
            status=OrganizationStatus.ACTIVE,
        )

    def inactive(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations that are inactive but
        have not been archived.
        """

        return self.filter(
            is_active=False,
        ).exclude(
            status=OrganizationStatus.ARCHIVED,
        )

    def archived(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations archived at the
        business lifecycle level.

        This does not mean soft-deleted. Archived
        organizations remain recoverable through the
        organization lifecycle unless explicitly
        soft-deleted.
        """

        return self.filter(
            status=OrganizationStatus.ARCHIVED,
            is_deleted=False,
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

        return self.filter(
            verification_status=VerificationStatus.VERIFIED,
        )

    def unverified(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations that are not yet verified.
        """

        return self.exclude(
            verification_status=VerificationStatus.VERIFIED,
        )

    def pending_verification(
        self,
    ) -> OrganizationQuerySet:
        """
        Return organizations awaiting verification.
        """

        return self.filter(
            verification_status=VerificationStatus.PENDING,
        )

    # ------------------------------------------------------------------
    # Tenant
    # ------------------------------------------------------------------

    def for_tenant(
        self,
        tenant,
    ) -> OrganizationQuerySet:
        """
        Return organizations belonging to the
        specified tenant.
        """

        return self.filter(
            tenant=tenant,
        )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def by_category(
        self,
        category: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization category.
        """

        return self.filter(
            category=category,
        )

    def by_type(
        self,
        organization_type: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization type.
        """

        return self.filter(
            organization_type=organization_type,
        )

    def by_status(
        self,
        status: str,
    ) -> OrganizationQuerySet:
        """
        Filter by lifecycle status.
        """

        return self.filter(
            status=status,
        )

    def by_size(
        self,
        size: str,
    ) -> OrganizationQuerySet:
        """
        Filter by organization size.
        """

        return self.filter(
            size=size,
        )

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    def demo(
        self,
    ) -> OrganizationQuerySet:
        """
        Return demo organizations.
        """

        return self.filter(
            is_demo=True,
        )

    def production(
        self,
    ) -> OrganizationQuerySet:
        """
        Return production organizations.
        """

        return self.filter(
            is_demo=False,
        )

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    def for_country(
        self,
        country: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by country.
        """

        return self.filter(
            country=country,
        )

    def for_state(
        self,
        state: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by state.
        """

        return self.filter(
            state=state,
        )

    def for_city(
        self,
        city: str,
    ) -> OrganizationQuerySet:
        """
        Filter organizations by city.
        """

        return self.filter(
            city=city,
        )

    # ------------------------------------------------------------------
    # Query Optimization
    # ------------------------------------------------------------------

    def with_related(
        self,
    ) -> OrganizationQuerySet:
        """
        Load commonly accessed related objects.

        Uses only relations that actually exist on
        the Organization model.
        """

        return self.select_related(
            "tenant",
        ).prefetch_related(
            "profile",
            "branding",
            "domains",
            "feature_entitlements",
            "module_entitlements",
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> OrganizationQuerySet:
        """
        Search organizations using common business
        identity and geographic fields.
        """

        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(
                name__icontains=query,
            )
            | models.Q(
                display_name__icontains=query,
            )
            | models.Q(
                code__icontains=query,
            )
            | models.Q(
                email__icontains=query,
            )
            | models.Q(
                phone__icontains=query,
            )
            | models.Q(
                registration_number__icontains=query,
            )
            | models.Q(
                website__icontains=query,
            )
            | models.Q(
                city__icontains=query,
            )
            | models.Q(
                state__icontains=query,
            )
            | models.Q(
                country__icontains=query,
            )
        ).distinct()


__all__: tuple[str, ...] = ("OrganizationQuerySet",)
