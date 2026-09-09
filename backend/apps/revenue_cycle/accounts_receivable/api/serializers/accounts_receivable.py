"""DRF serializers for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from rest_framework import serializers

from ...models import ARAccount, ARTransaction


class ARAccountSerializer(serializers.ModelSerializer):
    """Serialize read-only AR account state."""

    class Meta:
        """Configure the account serializer."""

        model = ARAccount
        fields = (
            "id",
            "organization",
            "patient",
            "account_number",
            "currency",
            "status",
            "balance_amount",
            "total_charges",
            "total_payments",
            "total_adjustments",
            "total_write_offs",
            "hold_reason",
            "hold_note",
            "opened_at",
            "closed_at",
            "version",
        )
        read_only_fields = fields


class ARTransactionSerializer(serializers.ModelSerializer):
    """Validate and serialize AR transaction requests."""

    class Meta:
        """Configure the transaction serializer."""

        model = ARTransaction
        fields = (
            "id",
            "account",
            "patient",
            "transaction_number",
            "transaction_type",
            "status",
            "amount",
            "transaction_date",
            "source_type",
            "source_id",
            "external_reference",
            "note",
            "reversed_at",
        )
        read_only_fields = (
            "id",
            "patient",
            "status",
            "reversed_at",
        )

    def validate_amount(self, value):
        """Require a strictly positive transaction amount."""

        if value <= 0:
            raise serializers.ValidationError(
                "Transaction amount must be greater than zero."
            )
        return value


__all__ = ("ARAccountSerializer", "ARTransactionSerializer")
