"""Claim scrubbing API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.claim_scrubbing.models import (
    ClaimScrub,
    ClaimScrubFinding,
    ScrubRule,
)


class ScrubRuleSerializer(serializers.ModelSerializer):
    """Serialize scrub rules."""

    class Meta:
        """Configure scrub rule serialization."""

        model = ScrubRule
        fields = (
            "id",
            "code",
            "name",
            "rule_type",
            "field_name",
            "configuration",
            "severity",
            "is_blocking",
            "priority",
        )
        read_only_fields = ("id",)


class ClaimScrubFindingSerializer(serializers.ModelSerializer):
    """Serialize scrub findings."""

    class Meta:
        """Configure finding serialization."""

        model = ClaimScrubFinding
        fields = (
            "id",
            "rule",
            "field_name",
            "message",
            "severity",
            "is_blocking",
            "is_resolved",
            "observed_value",
        )
        read_only_fields = fields


class ClaimScrubSerializer(serializers.ModelSerializer):
    """Serialize claim scrub aggregates and findings."""

    findings = ClaimScrubFindingSerializer(many=True, read_only=True)

    class Meta:
        """Configure scrub serialization."""

        model = ClaimScrub
        fields = (
            "id",
            "patient",
            "claim_reference",
            "idempotency_key",
            "status",
            "input_snapshot",
            "started_at",
            "completed_at",
            "override_reason",
            "findings",
        )
        read_only_fields = (
            "id",
            "status",
            "started_at",
            "completed_at",
            "override_reason",
            "findings",
        )


class CreateClaimScrubSerializer(serializers.Serializer):
    """Validate scrub creation input."""

    patient_id = serializers.UUIDField()
    claim_reference = serializers.CharField(max_length=120)
    idempotency_key = serializers.CharField(max_length=160)
    input_snapshot = serializers.JSONField()


__all__ = (
    "ScrubRuleSerializer",
    "ClaimScrubFindingSerializer",
    "ClaimScrubSerializer",
    "CreateClaimScrubSerializer",
)
