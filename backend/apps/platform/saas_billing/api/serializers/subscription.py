"""
SaaS Billing Subscription API serializers.

Handles:

- Subscription representation
- Subscription lifecycle data
- Plan information
- Entitlements
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    Subscription,
)


class SubscriptionSerializer(
    serializers.ModelSerializer,
):
    """
    Subscription read serializer.

    Used for:

    - Subscription details
    - Organization dashboard
    - Billing portal
    """

    plan_name = serializers.CharField(
        source="plan.name",
        read_only=True,
    )

    plan_code = serializers.CharField(
        source="plan.code",
        read_only=True,
    )

    billing_cycle = serializers.CharField(
        source="plan.billing_cycle",
        read_only=True,
    )

    class Meta:
        model = Subscription

        fields = [
            "id",
            "tenant",
            "organization",
            "plan",
            "plan_name",
            "plan_code",
            "billing_cycle",
            "status",
            "trial_start",
            "trial_end",
            "started_at",
            "current_period_start",
            "current_period_end",
            "expires_at",
            "grace_period_end",
            "auto_renew",
            "cancelled_at",
            "cancellation_reason",
            "plan_snapshot",
            "feature_snapshot",
            "seats_used",
            "usage_snapshot",
            "provider",
            "external_subscription_id",
            "metadata",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "tenant",
            "organization",
            "plan",
            "plan_name",
            "plan_code",
            "billing_cycle",
            "status",
            "trial_start",
            "trial_end",
            "started_at",
            "current_period_start",
            "current_period_end",
            "expires_at",
            "grace_period_end",
            "cancelled_at",
            "plan_snapshot",
            "feature_snapshot",
            "created_at",
            "updated_at",
        ]


class SubscriptionLifecycleSerializer(
    serializers.Serializer,
):
    """
    Subscription lifecycle action serializer.

    Used for:

    - Activate
    - Renew
    - Cancel
    - Upgrade
    - Downgrade
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    plan_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )


class SubscriptionCreateSerializer(
    serializers.Serializer,
):
    """
    Subscription creation serializer.

    Workflow:

    CreateSubscriptionWorkflow
    """

    plan_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )


__all__ = (
    "SubscriptionSerializer",
    "SubscriptionLifecycleSerializer",
    "SubscriptionCreateSerializer",
)
