"""
SaaS Billing Usage API serializers.

Handles:

- Usage record representation
- Usage collection requests
- Usage charging requests
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    Usage,
)


class UsageSerializer(
    serializers.ModelSerializer,
):
    """
    Usage record read serializer.

    Used for:

    - Usage dashboard
    - Billing analytics
    - Consumption reports
    """

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Usage

        fields = [
            "id",
            "organization",
            "organization_name",
            "department",
            "metric_type",
            "value",
            "unit",
            "is_billable",
            "billing_rate",
            "calculated_cost",
            "source",
            "reference_id",
            "metadata",
            "period_start",
            "period_end",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "organization",
            "calculated_cost",
            "created_at",
            "updated_at",
        ]


class UsageCreateSerializer(
    serializers.Serializer,
):
    """
    Usage collection serializer.

    Used by:

    CollectUsageWorkflow
    """

    metric_type = serializers.CharField(
        max_length=100,
    )

    value = serializers.DecimalField(
        max_digits=14,
        decimal_places=4,
    )

    department_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    module = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    source = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    reference_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    billable = serializers.BooleanField(
        default=False,
    )

    def validate_value(
        self,
        value: Decimal,
    ):
        """
        Validate usage amount.
        """

        if value < 0:
            raise serializers.ValidationError("Usage value cannot be negative.")

        return value


class UsageChargeSerializer(
    serializers.Serializer,
):
    """
    Usage charging serializer.

    Used by:

    ChargeUsageWorkflow
    """

    billing_rate = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )

    def validate_billing_rate(
        self,
        value: Decimal,
    ):
        """
        Validate billing rate.
        """

        if value <= 0:
            raise serializers.ValidationError("Billing rate must be greater than zero.")

        return value


class UsageEvaluationSerializer(
    serializers.Serializer,
):
    """
    Usage evaluation serializer.

    Used by:

    EvaluateUsageWorkflow
    """

    metric_type = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = (
    "UsageSerializer",
    "UsageCreateSerializer",
    "UsageChargeSerializer",
    "UsageEvaluationSerializer",
)
