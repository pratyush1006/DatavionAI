"""DRF serializers for Revenue Cycle integration records."""

from __future__ import annotations

from rest_framework import serializers

from ...models import RevenueCycleIntegrationRecord


class RevenueCycleIntegrationRecordSerializer(serializers.ModelSerializer):
    """Serialize integration records and validate their envelope."""

    class Meta:
        """Configure the integration record serializer."""

        model = RevenueCycleIntegrationRecord
        fields = (
            "id",
            "organization",
            "event_type",
            "source",
            "event_name",
            "aggregate_id",
            "idempotency_key",
            "payload",
            "status",
            "attempts",
            "last_error",
            "processed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "attempts",
            "last_error",
            "processed_at",
            "created_at",
            "updated_at",
        )

    def validate_idempotency_key(self, value):
        """Require a non-empty integration idempotency key."""

        if not value.strip():
            raise serializers.ValidationError("idempotency_key is required.")
        return value.strip()

    def validate_event_name(self, value):
        """Require a non-empty integration event name."""

        if not value.strip():
            raise serializers.ValidationError("event_name is required.")
        return value.strip()

    def validate_payload(self, value):
        """Require the event payload to be a JSON object."""

        if not isinstance(value, dict):
            raise serializers.ValidationError("payload must be an object.")
        return value


__all__ = ("RevenueCycleIntegrationRecordSerializer",)
