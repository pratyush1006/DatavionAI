"""
FinancialReport services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.financial_management.models import FinancialReport


class FinancialReportService:
    """
    Application service for financial_report write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> FinancialReport:
        """
        Create a new financial_report.
        """

        instance = FinancialReport(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: FinancialReport,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> FinancialReport:
        """
        Update an existing financial_report.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: FinancialReport,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a financial_report.
        """

        instance.hard_delete()


create_financial_report = FinancialReportService.create

update_financial_report = FinancialReportService.update

delete_financial_report = FinancialReportService.delete


__all__ = [
    "FinancialReportService",
    "create_financial_report",
    "update_financial_report",
    "delete_financial_report",
]
