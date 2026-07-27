"""
Insurance claim serializers for the Billing application.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.models import InsuranceClaim
from apps.billing.services import (
    create_claim,
    update_claim,
)
from apps.common.api.serializers import BaseModelSerializer


class InsuranceClaimBaseSerializer(BaseModelSerializer):
    """
    Base serializer containing shared normalization logic for insurance claim serializers.
    """

    class Meta:
        model = InsuranceClaim
        fields: tuple[str, ...] = ()

    def validate_claim_number(
        self,
        value: str,
    ) -> str:
        """
        Normalize the claim number.
        """

        return self._normalize_text(
            value,
        ).upper()

    def validate_claim_amount(
        self,
        value: Decimal,
    ) -> Decimal:
        """
        Validate that claim_amount is positive.
        """

        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Claim amount must be greater than zero.")

        return value


class InsuranceClaimListSerializer(InsuranceClaimBaseSerializer):
    """
    Serializer used for listing insurance claims.
    """

    class Meta(InsuranceClaimBaseSerializer.Meta):
        fields = (
            "id",
            "patient",
            "invoice",
            "insurance_provider",
            "policy_number",
            "claim_number",
            "claim_amount",
            "approved_amount",
            "status",
            "submitted_at",
            "is_active",
        )
        read_only_fields = (
            "id",
            "approved_amount",
            "submitted_at",
            "settled_at",
            "is_active",
            "created_at",
            "updated_at",
        )


class InsuranceClaimDetailSerializer(InsuranceClaimBaseSerializer):
    """
    Serializer used for retrieving insurance claim details.
    """

    class Meta(InsuranceClaimBaseSerializer.Meta):
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
        read_only_fields = (
            "id",
            "organization",
            "submitted_at",
            "settled_at",
            "is_active",
            "created_at",
            "updated_at",
        )


class InsuranceClaimCreateSerializer(InsuranceClaimBaseSerializer):
    """
    Serializer used for creating insurance claims.
    """

    class Meta(InsuranceClaimBaseSerializer.Meta):
        fields = (
            "patient",
            "invoice",
            "insurance_provider",
            "policy_number",
            "claim_number",
            "claim_amount",
            "status",
            "rejection_reason",
        )
        read_only_fields = (
            "id",
            "organization",
            "approved_amount",
            "submitted_at",
            "settled_at",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an insurance claim.
        """

        return create_claim(
            validated_data=validated_data,
        )


class InsuranceClaimUpdateSerializer(InsuranceClaimBaseSerializer):
    """
    Serializer used for updating insurance claims.
    """

    class Meta(InsuranceClaimBaseSerializer.Meta):
        fields = (
            "insurance_provider",
            "policy_number",
            "claim_amount",
            "approved_amount",
            "status",
            "rejection_reason",
        )
        read_only_fields = (
            "id",
            "organization",
            "patient",
            "invoice",
            "claim_number",
            "submitted_at",
            "settled_at",
            "is_active",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance: InsuranceClaim,
        validated_data: dict[str, object],
    ) -> InsuranceClaim:
        """
        Update an insurance claim.
        """

        return update_claim(
            instance=instance,
            validated_data=validated_data,
        )


class InsuranceClaimApproveSerializer(
    serializers.Serializer,
):
    """
    Serializer for approving an insurance claim.
    """

    approved_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )

    def validate_approved_amount(
        self,
        value: Decimal,
    ) -> Decimal:
        """
        Validate that approved_amount does not exceed claim_amount.
        """

        claim = self.context.get("claim")

        if claim and value > claim.claim_amount:
            raise serializers.ValidationError(
                "Approved amount cannot exceed the claim amount."
            )

        return value


class InsuranceClaimRejectSerializer(
    serializers.Serializer,
):
    """
    Serializer for rejecting an insurance claim.
    """

    rejection_reason = serializers.CharField(
        max_length=2000,
    )


__all__ = [
    "InsuranceClaimApproveSerializer",
    "InsuranceClaimBaseSerializer",
    "InsuranceClaimCreateSerializer",
    "InsuranceClaimDetailSerializer",
    "InsuranceClaimListSerializer",
    "InsuranceClaimRejectSerializer",
    "InsuranceClaimUpdateSerializer",
]
