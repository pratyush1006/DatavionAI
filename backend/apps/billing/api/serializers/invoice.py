"""
Invoice serializers for the Billing application.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.models import Invoice, InvoiceItem
from apps.billing.services import create_invoice, update_invoice
from apps.common.api.serializers import BaseModelSerializer


class InvoiceBaseSerializer(BaseModelSerializer):
    """
    Base serializer containing shared normalization logic for invoice serializers.
    """

    class Meta:
        model = Invoice
        fields: tuple[str, ...] = ()

    def validate_invoice_number(
        self,
        value: str,
    ) -> str:
        """
        Normalize the invoice number.
        """

        return self._normalize_text(
            value,
        ).upper()

    def validate_total_amount(
        self,
        value: Decimal,
    ) -> Decimal:
        """
        Validate that total_amount is positive.
        """

        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Total amount must be greater than zero.")

        return value


class InvoiceListSerializer(InvoiceBaseSerializer):
    """
    Serializer used for listing invoices.
    """

    class Meta(InvoiceBaseSerializer.Meta):
        fields = (
            "id",
            "invoice_number",
            "patient",
            "invoice_date",
            "due_date",
            "total_amount",
            "paid_amount",
            "balance_amount",
            "status",
            "is_active",
        )
        read_only_fields = (
            "id",
            "paid_amount",
            "balance_amount",
            "is_active",
            "created_at",
            "updated_at",
        )


class InvoiceDetailSerializer(InvoiceBaseSerializer):
    """
    Serializer used for retrieving invoice details.
    """

    items = serializers.SerializerMethodField()

    class Meta(InvoiceBaseSerializer.Meta):
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
        read_only_fields = (
            "id",
            "paid_amount",
            "balance_amount",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_items(
        self,
        instance: Invoice,
    ) -> list[dict[str, object]]:
        """
        Return the invoice line items.
        """

        items = instance.items.filter(
            is_active=True,
        )

        serializer = InvoiceItemSerializer(
            items,
            many=True,
        )

        return serializer.data


class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    Serializer for invoice line items.
    """

    class Meta:
        model = InvoiceItem
        fields = (
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "total_price",
            "service_code",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "total_price",
            "is_active",
            "created_at",
            "updated_at",
        )


class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating invoice line items.
    """

    class Meta:
        model = InvoiceItem
        fields = (
            "description",
            "quantity",
            "unit_price",
            "service_code",
        )

    def validate_quantity(
        self,
        value: int,
    ) -> int:
        """
        Validate that quantity is positive.
        """

        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")

        return value

    def validate_unit_price(
        self,
        value: Decimal,
    ) -> Decimal:
        """
        Validate that unit_price is non-negative.
        """

        if value < Decimal("0.00"):
            raise serializers.ValidationError("Unit price cannot be negative.")

        return value


class InvoiceCreateSerializer(InvoiceBaseSerializer):
    """
    Serializer used for creating invoices.
    """

    items = InvoiceItemCreateSerializer(
        many=True,
        required=False,
    )

    class Meta(InvoiceBaseSerializer.Meta):
        fields = (
            "organization",
            "patient",
            "invoice_number",
            "invoice_date",
            "due_date",
            "total_amount",
            "balance_amount",
            "status",
            "notes",
            "items",
        )
        read_only_fields = (
            "id",
            "paid_amount",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an invoice.
        """

        items = validated_data.pop(
            "items",
            None,
        )

        return create_invoice(
            validated_data=validated_data,
            items=items,
        )


class InvoiceUpdateSerializer(InvoiceBaseSerializer):
    """
    Serializer used for updating invoices.
    """

    class Meta(InvoiceBaseSerializer.Meta):
        fields = (
            "invoice_number",
            "invoice_date",
            "due_date",
            "total_amount",
            "balance_amount",
            "status",
            "notes",
        )
        read_only_fields = (
            "id",
            "organization",
            "patient",
            "paid_amount",
            "is_active",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance: Invoice,
        validated_data: dict[str, object],
    ) -> Invoice:
        """
        Update an invoice.
        """

        return update_invoice(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "InvoiceBaseSerializer",
    "InvoiceCreateSerializer",
    "InvoiceDetailSerializer",
    "InvoiceItemCreateSerializer",
    "InvoiceItemSerializer",
    "InvoiceListSerializer",
    "InvoiceUpdateSerializer",
]
