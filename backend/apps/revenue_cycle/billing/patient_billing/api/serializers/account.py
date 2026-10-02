"""Patient Billing account API serializers."""

from __future__ import annotations

from decimal import Decimal

from apps.revenue_cycle.billing.patient_billing.models import PatientBillingAccount
from rest_framework import serializers


class PatientBillingAccountSerializer(serializers.ModelSerializer):
    """Serialize patient billing accounts."""

    class Meta:
        """Serializer metadata."""

        model = PatientBillingAccount
        fields = (
            "id",
            "organization",
            "patient",
            "account_number",
            "status",
            "currency",
            "opening_balance",
            "credit_limit",
            "current_balance",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "opening_balance",
            "current_balance",
            "is_active",
            "created_at",
            "updated_at",
        )


class PatientBillingAccountCreateSerializer(serializers.ModelSerializer):
    """Validate patient billing account creation."""

    class Meta:
        """Serializer metadata."""

        model = PatientBillingAccount
        fields = (
            "patient",
            "account_number",
            "currency",
            "opening_balance",
            "credit_limit",
            "notes",
        )

    def validate_account_number(self, value: str) -> str:
        """Require a non-empty normalized account number."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Account number is required.",
            )
        return value

    def validate_opening_balance(self, value: Decimal) -> Decimal:
        """Reject negative opening balances."""

        if value < Decimal("0.00"):
            raise serializers.ValidationError(
                "Opening balance cannot be negative.",
            )
        return value

    def validate_credit_limit(self, value: Decimal) -> Decimal:
        """Reject negative credit limits."""

        if value < Decimal("0.00"):
            raise serializers.ValidationError(
                "Credit limit cannot be negative.",
            )
        return value


class PatientBillingAccountUpdateSerializer(serializers.ModelSerializer):
    """Validate mutable patient billing account fields."""

    class Meta:
        """Serializer metadata."""

        model = PatientBillingAccount
        fields = (
            "currency",
            "credit_limit",
            "notes",
        )


class PatientBillingAccountTransitionSerializer(serializers.Serializer):
    """Validate account lifecycle transitions."""

    status = serializers.ChoiceField(
        choices=PatientBillingAccount._meta.get_field("status").choices,
    )


__all__ = (
    "PatientBillingAccountCreateSerializer",
    "PatientBillingAccountSerializer",
    "PatientBillingAccountTransitionSerializer",
    "PatientBillingAccountUpdateSerializer",
)
