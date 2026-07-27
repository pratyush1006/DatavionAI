"""
Vendor selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.accounts_payable.models import Vendor
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class VendorSelector:
    """
    Read-only queries for vendor.
    """

    @staticmethod
    def queryset() -> QuerySet[Vendor]:
        """
        Return the base vendor queryset.
        """

        return Vendor.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[Vendor]:
        """
        Return all vendor records.
        """

        return VendorSelector.queryset()

    @staticmethod
    def get(
        *,
        vendor_id: UUID,
    ) -> Vendor:
        """
        Return a vendor by identifier.
        """

        return get_object_or_404(
            VendorSelector.queryset(),
            pk=vendor_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Vendor]:
        """
        Return all vendor records for an organization.
        """

        return VendorSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        vendor_id: UUID,
    ) -> bool:
        """
        Determine whether a vendor exists.
        """

        return (
            VendorSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=vendor_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of vendor records for an organization.
        """

        return VendorSelector.list_by_organization(
            organization=organization,
        ).count()


get_vendors = VendorSelector.list

get_vendor_by_id = VendorSelector.get

get_organization_vendors = VendorSelector.list_by_organization


__all__ = [
    "VendorSelector",
    "get_vendor_by_id",
    "get_vendors",
    "get_organization_vendors",
]
