"""Patient statement API serializers."""

from __future__ import annotations

from apps.revenue_cycle.billing.patient_billing.models import PatientBillingStatement
from rest_framework import serializers


class PatientBillingStatementSerializer(serializers.ModelSerializer):
    """Serialize patient billing statements."""

    class Meta:
        """Serializer metadata."""

        model = PatientBillingStatement
        fields = (
            "id",
            "account",
            "statement_number",
            "period_start",
            "period_end",
            "opening_balance",
            "charges",
            "payments",
            "adjustments",
            "closing_balance",
            "status",
            "issued_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "account",
            "statement_number",
            "opening_balance",
            "charges",
            "payments",
            "adjustments",
            "closing_balance",
            "status",
            "issued_at",
            "created_at",
            "updated_at",
        )


class PatientBillingStatementCreateSerializer(serializers.Serializer):
    """Validate statement generation input."""

    account_id = serializers.UUIDField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()

    def validate(self, attrs: dict) -> dict:
        """Require an ordered statement period."""

        if attrs["period_end"] < attrs["period_start"]:
            raise serializers.ValidationError(
                "period_end cannot precede period_start.",
            )
        return attrs


__all__ = (
    "PatientBillingStatementCreateSerializer",
    "PatientBillingStatementSerializer",
)
