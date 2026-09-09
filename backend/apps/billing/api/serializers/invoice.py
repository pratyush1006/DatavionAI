"""
Billing Core Invoice API serializers.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.models import Invoice, InvoiceItem


class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    """Validate invoice line-item input."""

    class Meta:
        """Serializer metadata."""

        model = InvoiceItem
        fields = ("description", "quantity", "unit_price", "service_code")

    def validate_quantity(self, value: int) -> int:
        """Require positive quantity."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_unit_price(self, value: Decimal) -> Decimal:
        """Reject negative unit prices."""
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Unit price cannot be negative.")
        return value


class InvoiceCreateSerializer(serializers.Serializer):
    """Validate invoice creation input."""

    patient = serializers.UUIDField()
    invoice_number = serializers.CharField(max_length=50)
    invoice_date = serializers.DateField()
    due_date = serializers.DateField()
    total_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.00")
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    items = InvoiceItemCreateSerializer(many=True, required=False)

    def validate_invoice_number(self, value: str) -> str:
        """Normalize invoice number."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Invoice number cannot be empty.")
        return value

    def validate(self, attrs: dict) -> dict:
        """Validate invoice date ordering."""
        if attrs["due_date"] < attrs["invoice_date"]:
            raise serializers.ValidationError("Due date cannot be before invoice date.")
        return attrs


class InvoiceUpdateSerializer(serializers.Serializer):
    """Validate mutable invoice fields."""

    invoice_date = serializers.DateField(required=False)
    due_date = serializers.DateField(required=False)
    total_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.00"), required=False
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class InvoiceListSerializer(serializers.ModelSerializer):
    """Serialize invoice collection records."""

    class Meta:
        """Serializer metadata."""

        model = Invoice
        fields = (
            "id",
            "organization",
            "patient",
            "invoice_number",
            "invoice_date",
            "due_date",
            "total_amount",
            "paid_amount",
            "balance_amount",
            "status",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """Serialize one invoice with line items."""

    items = InvoiceItemCreateSerializer(many=True, read_only=True)

    class Meta:
        """Serializer metadata."""

        model = Invoice
        fields = (
            "id",
            "organization",
            "patient",
            "invoice_number",
            "invoice_date",
            "due_date",
            "total_amount",
            "paid_amount",
            "balance_amount",
            "status",
            "notes",
            "items",
            "is_active",
            "created_at",
            "updated_at",
        )


__all__ = (
    "InvoiceCreateSerializer",
    "InvoiceDetailSerializer",
    "InvoiceItemCreateSerializer",
    "InvoiceListSerializer",
    "InvoiceUpdateSerializer",
)
