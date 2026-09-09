from __future__ import annotations

"""DRF serializers for Revenue Cycle Coding."""

from rest_framework import serializers

from ...constants import CodeSystem, CodingStatus, CodingType
from ...models import CodeAssignment, CodingRecord


class CodeAssignmentSerializer(serializers.ModelSerializer):
    """Serialize a Coding code assignment."""

    class Meta:
        """Define CodeAssignment serializer metadata."""

        model = CodeAssignment
        fields = (
            "id",
            "code_system",
            "code",
            "description",
            "sequence",
            "present_on_admission",
            "is_primary",
            "evidence",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class CodingRecordSerializer(serializers.ModelSerializer):
    """Serialize Coding record responses."""

    patient_id = serializers.UUIDField(read_only=True)
    status = serializers.ChoiceField(
        choices=CodingStatus.choices,
        read_only=True,
    )
    code_assignments = CodeAssignmentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """Define CodingRecord response serializer metadata."""

        model = CodingRecord
        fields = (
            "id",
            "organization",
            "patient_id",
            "coding_type",
            "status",
            "source_reference",
            "service_date",
            "encounter_type",
            "clinical_summary",
            "documentation",
            "coding_notes",
            "rejection_reason",
            "idempotency_key",
            "assigned_to",
            "reviewed_by",
            "validated_by",
            "released_by",
            "assigned_at",
            "reviewed_at",
            "validated_at",
            "released_at",
            "voided_at",
            "code_assignments",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CodingCreateSerializer(serializers.Serializer):
    """Validate Coding record creation requests."""

    patient_id = serializers.UUIDField()
    coding_type = serializers.ChoiceField(
        choices=CodingType.choices,
    )
    source_reference = serializers.CharField(
        max_length=128,
    )
    service_date = serializers.DateField()
    encounter_type = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
    )
    clinical_summary = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    documentation = serializers.JSONField(
        required=False,
    )
    coding_notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    idempotency_key = serializers.CharField(
        max_length=128,
    )


class CodingUpdateSerializer(serializers.Serializer):
    """Validate mutable Coding record fields."""

    encounter_type = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
    )
    clinical_summary = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    documentation = serializers.JSONField(
        required=False,
    )
    coding_notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    rejection_reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class CodingTransitionSerializer(serializers.Serializer):
    """Validate a Coding lifecycle transition."""

    target_status = serializers.ChoiceField(
        choices=CodingStatus.choices,
    )
    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class CodeAssignmentCreateSerializer(serializers.Serializer):
    """Validate a code assignment request."""

    code_system = serializers.ChoiceField(
        choices=CodeSystem.choices,
    )
    code = serializers.CharField(max_length=64)
    description = serializers.CharField(
        max_length=512,
        required=False,
        allow_blank=True,
    )
    sequence = serializers.IntegerField(
        min_value=1,
        default=1,
    )
    is_primary = serializers.BooleanField(
        default=False,
    )
    present_on_admission = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    evidence = serializers.JSONField(
        required=False,
    )


__all__ = (
    "CodeAssignmentCreateSerializer",
    "CodeAssignmentSerializer",
    "CodingCreateSerializer",
    "CodingRecordSerializer",
    "CodingTransitionSerializer",
    "CodingUpdateSerializer",
)
