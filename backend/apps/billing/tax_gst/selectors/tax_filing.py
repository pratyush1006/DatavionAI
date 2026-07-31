"""
TaxFiling selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.tax_gst.models import TaxFiling
from apps.platform.organizations.models import Organization


class TaxFilingSelector:
    """
    Read-only queries for tax_filing.
    """

    @staticmethod
    def queryset() -> QuerySet[TaxFiling]:
        """
        Return the base tax_filing queryset.
        """

        return TaxFiling.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[TaxFiling]:
        """
        Return all tax_filing records.
        """

        return TaxFilingSelector.queryset()

    @staticmethod
    def get(
        *,
        tax_filing_id: UUID,
    ) -> TaxFiling:
        """
        Return a tax_filing by identifier.
        """

        return get_object_or_404(
            TaxFilingSelector.queryset(),
            pk=tax_filing_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[TaxFiling]:
        """
        Return all tax_filing records for an organization.
        """

        return TaxFilingSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        tax_filing_id: UUID,
    ) -> bool:
        """
        Determine whether a tax_filing exists.
        """

        return (
            TaxFilingSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=tax_filing_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of tax_filing records for an organization.
        """

        return TaxFilingSelector.list_by_organization(
            organization=organization,
        ).count()


get_tax_filings = TaxFilingSelector.list

get_tax_filing_by_id = TaxFilingSelector.get

get_organization_tax_filings = TaxFilingSelector.list_by_organization


__all__ = [
    "TaxFilingSelector",
    "get_tax_filing_by_id",
    "get_tax_filings",
    "get_organization_tax_filings",
]
