"""Serializers for Revenue Cycle Electronic Remittance Advice."""

from __future__ import annotations

from rest_framework import serializers

from ...models import ERA


class ERAInputSerializer(serializers.Serializer):
    """Validate ERA creation input."""

    patient_id = serializers.UUIDField(required=False, allow_null=True)
    payer_name = serializers.CharField(max_length=200)
    payer_identifier = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    trace_number = serializers.CharField(max_length=100)
    check_or_eft_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    source = serializers.ChoiceField(
        choices=[value for value, _label in ERA._meta.get_field("source").choices],
        required=False,
    )
    payment_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        required=False,
    )
    adjustment_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        required=False,
    )
    received_at = serializers.DateTimeField()
    external_reference = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    idempotency_key = serializers.CharField(max_length=150)
    raw_payload = serializers.JSONField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)


class ERAOutputSerializer(serializers.ModelSerializer):
    """Serialize an ERA aggregate for API responses."""

    class Meta:
        """Configure serialized ERA fields."""

        model = ERA
        fields = (
            "id",
            "patient",
            "payer_name",
            "payer_identifier",
            "trace_number",
            "check_or_eft_number",
            "source",
            "status",
            "payment_amount",
            "adjustment_amount",
            "received_at",
            "validated_at",
            "posted_at",
            "reversed_at",
            "external_reference",
            "idempotency_key",
            "validation_errors",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "validated_at",
            "posted_at",
            "reversed_at",
            "validation_errors",
            "created_at",
            "updated_at",
        )


__all__ = ("ERAInputSerializer", "ERAOutputSerializer")
