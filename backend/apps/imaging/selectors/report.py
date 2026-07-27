"""
Imaging report selector.
"""

from __future__ import annotations

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.imaging.models import Report
from apps.platform.organizations.models import Organization


class ReportSelector:
    """
    Read-only queries for imaging reports.
    """

    @staticmethod
    def queryset() -> QuerySet[Report]:
        """
        Return the base report queryset.
        """

        return Report.objects.select_related(
            "study__patient",
            "reported_by",
        )

    @staticmethod
    def list() -> QuerySet[Report]:
        """
        Return all reports.
        """

        return ReportSelector.queryset()

    @staticmethod
    def get(
        *,
        report_id: str,
    ) -> Report:
        """
        Return a report by identifier.
        """

        return get_object_or_404(
            ReportSelector.queryset(),
            pk=report_id,
        )

    @staticmethod
    def list_by_study(
        *,
        study_id: str,
    ) -> QuerySet[Report]:
        """
        Return all reports for a given study.
        """

        return ReportSelector.queryset().filter(
            study_id=study_id,
        )

    @staticmethod
    def list_by_radiologist(
        *,
        employee_id: str,
    ) -> QuerySet[Report]:
        """
        Return all reports authored by a given radiologist.
        """

        return ReportSelector.queryset().filter(
            reported_by_id=employee_id,
        )

    @staticmethod
    def search(
        *,
        query: str,
    ) -> QuerySet[Report]:
        """
        Search reports by text content.
        """

        return ReportSelector.queryset().filter(
            Q(
                report_text__icontains=query,
            )
            | Q(
                findings__icontains=query,
            )
            | Q(
                impression__icontains=query,
            )
            | Q(
                recommendations__icontains=query,
            ),
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of reports within an organization.
        """

        return (
            ReportSelector.queryset()
            .filter(
                study__organization=organization,
            )
            .count()
        )


__all__ = [
    "ReportSelector",
]
