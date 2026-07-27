"""
List serializer for the FinancialReport model.
"""

from __future__ import annotations

from .base_financial_report import FinancialReportBaseSerializer
from .fields_financial_report import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class FinancialReportListSerializer(FinancialReportBaseSerializer):
    """
    Serializer used for listing financial_report records.
    """

    class Meta(FinancialReportBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "FinancialReportListSerializer",
]
