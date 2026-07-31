"""
Base serializer for the FinancialReport model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.financial_management.models import FinancialReport


class FinancialReportBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for financial_report serializers.
    """

    class Meta:
        model = FinancialReport
        fields: tuple[str, ...] = ()


__all__ = [
    "FinancialReportBaseSerializer",
]
