"""
Create serializer for the FinancialReport model.
"""

from __future__ import annotations

from apps.billing.financial_management.services import create_financial_report

from .base_financial_report import FinancialReportBaseSerializer
from .fields_financial_report import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class FinancialReportCreateSerializer(FinancialReportBaseSerializer):
    """
    Serializer used for creating financial_report records.
    """

    class Meta(FinancialReportBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a financial_report.
        """

        return create_financial_report(
            validated_data=validated_data,
        )


__all__ = [
    "FinancialReportCreateSerializer",
]
