"""
DatavionOS SaaS Billing Plan API serializers.

Provides API contracts for:

- Public pricing catalog
- Plan details
- Internal plan management
- Plan creation
- Plan updates

Architecture:

Plan Model
    |
Serializer Validation
    |
Workflow
    |
Service
    |
Domain Event
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    Plan,
)

# =============================================================================
# Public Plan Serializer
# =============================================================================


class PublicPlanSerializer(
    serializers.ModelSerializer,
):
    """
    Public subscription plan representation.

    Used by:

    - Pricing page
    - Signup flow
    - Organization onboarding
    """

    class Meta:
        model = Plan

        fields = (
            "id",
            "name",
            "code",
            "description",
            "plan_type",
            "healthcare_segment",
            "price",
            "currency",
            "billing_cycle",
            "trial_days",
            "annual_discount_percentage",
            "features",
            "modules",
            "limits",
            "is_featured",
        )

        read_only_fields = fields


# =============================================================================
# Plan Detail Serializer
# =============================================================================


class PlanDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Complete plan detail representation.

    Used by:

    - Plan detail API
    - Subscription selection flow
    """

    class Meta:
        model = Plan

        fields = (
            "id",
            "name",
            "code",
            "description",
            # Classification
            "plan_type",
            "healthcare_segment",
            # Pricing
            "price",
            "setup_fee",
            "currency",
            "billing_cycle",
            "trial_days",
            "annual_discount_percentage",
            # Organization limits
            "max_users",
            "max_branches",
            "max_doctors",
            # Healthcare limits
            "max_patients",
            "max_lab_orders",
            "max_imaging_orders",
            # Pharmacy limits
            "max_pharmacy_products",
            "max_inventory_transactions",
            # Platform limits
            "max_storage_gb",
            "max_api_requests",
            # AI limits
            "max_ai_requests",
            "max_ai_tokens",
            # Entitlements
            "features",
            "modules",
            "limits",
            "metadata",
            # Lifecycle
            "is_active",
            "is_public",
            "is_featured",
            "is_default",
            "is_custom",
            "display_order",
        )

        read_only_fields = fields


# =============================================================================
# Admin Plan Serializer
# =============================================================================


class PlanAdminSerializer(
    serializers.ModelSerializer,
):
    """
    Internal administration serializer.

    Used by:

    - Platform admins
    - SaaS operations team
    """

    class Meta:
        model = Plan

        fields = (
            "id",
            "name",
            "code",
            "description",
            "plan_type",
            "healthcare_segment",
            "price",
            "setup_fee",
            "currency",
            "billing_cycle",
            "trial_days",
            "annual_discount_percentage",
            "max_users",
            "max_branches",
            "max_doctors",
            "max_patients",
            "max_lab_orders",
            "max_imaging_orders",
            "max_pharmacy_products",
            "max_inventory_transactions",
            "max_storage_gb",
            "max_api_requests",
            "max_ai_requests",
            "max_ai_tokens",
            "features",
            "modules",
            "limits",
            "metadata",
            "is_active",
            "is_public",
            "is_featured",
            "is_default",
            "is_custom",
            "display_order",
        )


# =============================================================================
# Create Plan Serializer
# =============================================================================


class PlanCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Create SaaS plan serializer.

    Used by:

    - Platform administration
    - SaaS catalog management

    Flow:

    API
     |
    Serializer
     |
    CreatePlanWorkflow
    """

    class Meta:
        model = Plan

        fields = (
            "name",
            "code",
            "description",
            "plan_type",
            "healthcare_segment",
            "price",
            "setup_fee",
            "currency",
            "billing_cycle",
            "trial_days",
            "annual_discount_percentage",
            "max_users",
            "max_branches",
            "max_doctors",
            "max_patients",
            "max_lab_orders",
            "max_imaging_orders",
            "max_pharmacy_products",
            "max_inventory_transactions",
            "max_storage_gb",
            "max_api_requests",
            "max_ai_requests",
            "max_ai_tokens",
            "features",
            "modules",
            "limits",
            "metadata",
            "is_public",
            "is_featured",
            "is_default",
            "is_custom",
            "display_order",
        )


# =============================================================================
# Update Plan Serializer
# =============================================================================


class PlanUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Update SaaS plan serializer.

    Used by:

    - Platform administration
    - SaaS operations
    """

    class Meta:
        model = Plan

        fields = (
            "name",
            "description",
            "price",
            "setup_fee",
            "currency",
            "billing_cycle",
            "trial_days",
            "annual_discount_percentage",
            "features",
            "modules",
            "limits",
            "metadata",
            "is_public",
            "is_featured",
            "display_order",
        )


__all__ = [
    "PublicPlanSerializer",
    "PlanDetailSerializer",
    "PlanAdminSerializer",
    "PlanCreateSerializer",
    "PlanUpdateSerializer",
]
