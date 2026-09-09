"""
Billing Core Insurance Claim API serializers.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.models import InsuranceClaim


class InsuranceClaimCreateSerializer(serializers.Serializer):
    """Validate claim submission input."""

    patient = serializers.UUIDField()
    invoice = serializers.UUIDField()
    insurance_provider = serializers.CharField(max_length=255)
    policy_number = serializers.CharField(max_length=100)
    claim_number = serializers.CharField(max_length=50)
    claim_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )


class InsuranceClaimApproveSerializer(serializers.Serializer):
    """Validate claim approval input."""

    approved_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )


class InsuranceClaimRejectSerializer(serializers.Serializer):
    """Validate claim rejection input."""

    rejection_reason = serializers.CharField(max_length=2000)

    def validate_rejection_reason(self, value: str) -> str:
        """Require a non-empty reason."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Rejection reason is required.")
        return value


class InsuranceClaimListSerializer(serializers.ModelSerializer):
    """Serialize claim collections."""

    class Meta:
        """Serializer metadata."""

        model = InsuranceClaim
        fields = (
            "id",
            "organization",
            "patient",
            "invoice",
            "insurance_provider",
            "policy_number",
            "claim_number",
            "claim_amount",
            "approved_amount",
            "status",
            "submitted_at",
            "settled_at",
            "rejection_reason",
            "is_active",
            "created_at",
            "updated_at",
        )


class InsuranceClaimDetailSerializer(InsuranceClaimListSerializer):
    """Serialize one insurance claim."""


__all__ = (
    "InsuranceClaimApproveSerializer",
    "InsuranceClaimCreateSerializer",
    "InsuranceClaimDetailSerializer",
    "InsuranceClaimListSerializer",
    "InsuranceClaimRejectSerializer",
)
