"""Denial API serializers."""

from __future__ import annotations

from rest_framework import serializers

from ...constants import DenialStatus
from ...models import Denial


class DenialSerializer(serializers.ModelSerializer):
    """Serialize Denial instances for the REST API."""

    class Meta:
        """Serializer metadata."""

        model = Denial
        fields = (
            "id",
            "organization",
            "patient",
            "status",
            "priority",
            "reason_code",
            "reason_description",
            "payer_name",
            "denied_amount",
            "denied_at",
            "resolution_notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "denied_at",
            "created_at",
            "updated_at",
        )


class DenialTransitionSerializer(serializers.Serializer):
    """Validate a denial lifecycle transition request."""

    target_status = serializers.ChoiceField(choices=DenialStatus.choices)
    note = serializers.CharField(required=False, allow_blank=True)


__all__ = ("DenialSerializer", "DenialTransitionSerializer")
