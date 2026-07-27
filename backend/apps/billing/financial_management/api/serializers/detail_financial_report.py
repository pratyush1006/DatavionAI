"""
Detail serializer for the FinancialReport model.
"""

from __future__ import annotations

from .base_financial_report import FinancialReportBaseSerializer
from .fields_financial_report import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class FinancialReportDetailSerializer(FinancialReportBaseSerializer):
    """
    Serializer used for retrieving financial_report details.
    """

    class Meta(FinancialReportBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "FinancialReportDetailSerializer",
]
