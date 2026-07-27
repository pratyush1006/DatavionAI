"""
Update serializer for the FinancialReport model.
"""

from __future__ import annotations

from apps.billing.financial_management.models import FinancialReport
from apps.billing.financial_management.services import update_financial_report

from .base_financial_report import FinancialReportBaseSerializer
from .fields_financial_report import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class FinancialReportUpdateSerializer(FinancialReportBaseSerializer):
    """
    Serializer used for updating financial_report records.
    """

    class Meta(FinancialReportBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: FinancialReport,
        validated_data: dict[str, object],
    ) -> FinancialReport:
        """
        Update a financial_report.
        """

        return update_financial_report(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "FinancialReportUpdateSerializer",
]
