"""
Revenue Cycle Appeals API serializer exports.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from rest_framework import serializers

from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.appeals.constants import AppealStatus
from apps.revenue_cycle.appeals.models import Appeal


class AppealSerializer(serializers.ModelSerializer):
    """Serialize and validate Revenue Cycle Appeals."""

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
    )

    class Meta:
        """Configure the appeal serializer."""

        model = Appeal
        fields = (
            "id",
            "organization",
            "patient",
            "claim_reference",
            "payer_name",
            "appeal_number",
            "denial_reference",
            "status",
            "priority",
            "reason",
            "clinical_summary",
            "requested_amount",
            "approved_amount",
            "submitted_at",
            "decided_at",
            "decision_reason",
            "created_by",
            "updated_by",
            "idempotency_key",
            "metadata",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "submitted_at",
            "decided_at",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "is_deleted",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate appeal monetary and lifecycle invariants."""
        requested = attrs.get(
            "requested_amount",
            getattr(
                self.instance,
                "requested_amount",
                Decimal("0.00"),
            ),
        )
        approved = attrs.get(
            "approved_amount",
            getattr(
                self.instance,
                "approved_amount",
                Decimal("0.00"),
            ),
        )

        if requested < 0 or approved < 0:
            raise serializers.ValidationError("Appeal amounts cannot be negative.")
        if approved > requested:
            raise serializers.ValidationError(
                "approved_amount cannot exceed requested_amount."
            )

        if self.instance and self.instance.status in {
            AppealStatus.APPROVED,
            AppealStatus.PARTIALLY_APPROVED,
            AppealStatus.DENIED,
            AppealStatus.WITHDRAWN,
            AppealStatus.CLOSED,
        }:
            protected = {key for key in attrs if key not in {"metadata"}}
            if protected:
                raise serializers.ValidationError(
                    "Terminal appeals cannot be modified."
                )

        return attrs


class AppealTransitionSerializer(serializers.Serializer):
    """Validate an appeal lifecycle transition request."""

    status = serializers.ChoiceField(
        choices=AppealStatus.choices,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = (
    "AppealSerializer",
    "AppealTransitionSerializer",
)
