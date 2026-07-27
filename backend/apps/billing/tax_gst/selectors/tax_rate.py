"""
TaxRate selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.tax_gst.models import TaxRate
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class TaxRateSelector:
    """
    Read-only queries for tax_rate.
    """

    @staticmethod
    def queryset() -> QuerySet[TaxRate]:
        """
        Return the base tax_rate queryset.
        """

        return TaxRate.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[TaxRate]:
        """
        Return all tax_rate records.
        """

        return TaxRateSelector.queryset()

    @staticmethod
    def get(
        *,
        tax_rate_id: UUID,
    ) -> TaxRate:
        """
        Return a tax_rate by identifier.
        """

        return get_object_or_404(
            TaxRateSelector.queryset(),
            pk=tax_rate_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[TaxRate]:
        """
        Return all tax_rate records for an organization.
        """

        return TaxRateSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        tax_rate_id: UUID,
    ) -> bool:
        """
        Determine whether a tax_rate exists.
        """

        return (
            TaxRateSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=tax_rate_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of tax_rate records for an organization.
        """

        return TaxRateSelector.list_by_organization(
            organization=organization,
        ).count()


get_tax_rates = TaxRateSelector.list

get_tax_rate_by_id = TaxRateSelector.get

get_organization_tax_rates = TaxRateSelector.list_by_organization


__all__ = [
    "TaxRateSelector",
    "get_tax_rate_by_id",
    "get_tax_rates",
    "get_organization_tax_rates",
]
