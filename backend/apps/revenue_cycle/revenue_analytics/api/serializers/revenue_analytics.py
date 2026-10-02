"""DRF serializers for Revenue Analytics."""

from __future__ import annotations

from rest_framework import serializers

from ...models import RevenueMetricSnapshot


class RevenueMetricSnapshotSerializer(serializers.ModelSerializer):
    """Serialize Revenue Analytics KPI snapshots."""

    class Meta:
        """Configure the analytics snapshot serializer."""

        model = RevenueMetricSnapshot
        fields = (
            "id",
            "organization",
            "period",
            "period_start",
            "period_end",
            "gross_charges",
            "payments",
            "adjustments",
            "denials",
            "write_offs",
            "outstanding_ar",
            "encounter_count",
            "claim_count",
            "denied_claim_count",
            "paid_claim_count",
            "generated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "generated_at",
        )


__all__ = ("RevenueMetricSnapshotSerializer",)
