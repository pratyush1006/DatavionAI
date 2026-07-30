"""
FinancialReport selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.financial_management.models import FinancialReport
from apps.platform.organizations.models import Organization


class FinancialReportSelector:
    """
    Read-only queries for financial_report.
    """

    @staticmethod
    def queryset() -> QuerySet[FinancialReport]:
        """
        Return the base financial_report queryset.
        """

        return FinancialReport.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[FinancialReport]:
        """
        Return all financial_report records.
        """

        return FinancialReportSelector.queryset()

    @staticmethod
    def get(
        *,
        financial_report_id: UUID,
    ) -> FinancialReport:
        """
        Return a financial_report by identifier.
        """

        return get_object_or_404(
            FinancialReportSelector.queryset(),
            pk=financial_report_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[FinancialReport]:
        """
        Return all financial_report records for an organization.
        """

        return FinancialReportSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        financial_report_id: UUID,
    ) -> bool:
        """
        Determine whether a financial_report exists.
        """

        return (
            FinancialReportSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=financial_report_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of financial_report records for an organization.
        """

        return FinancialReportSelector.list_by_organization(
            organization=organization,
        ).count()


get_financial_reports = FinancialReportSelector.list

get_financial_report_by_id = FinancialReportSelector.get

get_organization_financial_reports = FinancialReportSelector.list_by_organization


__all__ = [
    "FinancialReportSelector",
    "get_financial_report_by_id",
    "get_financial_reports",
    "get_organization_financial_reports",
]
