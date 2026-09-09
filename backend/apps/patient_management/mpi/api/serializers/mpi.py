"""
Master Patient Index API serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.mpi.models import (
    MPIMatchCandidate,
    MPIRecord,
)


class MPIListSerializer(serializers.ModelSerializer):
    """Serialize compact MPI record representations."""

    class Meta:
        """Serializer metadata."""

        model = MPIRecord
        fields = (
            "id",
            "patient",
            "enterprise_identifier",
            "status",
            "match_score",
            "confidence",
        )
        read_only_fields = fields


class MPIDetailSerializer(serializers.ModelSerializer):
    """Serialize detailed MPI records."""

    class Meta:
        """Serializer metadata."""

        model = MPIRecord
        fields = (
            "id",
            "organization",
            "patient",
            "enterprise_identifier",
            "status",
            "source_system",
            "source_patient_identifier",
            "match_score",
            "confidence",
            "demographics_snapshot",
            "reviewed_at",
            "reviewed_by_id",
            "merged_into",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
        )
        read_only_fields = (
            "id",
            "status",
            "reviewed_at",
            "reviewed_by_id",
            "merged_into",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
        )


class MPICreateSerializer(serializers.Serializer):
    """Validate MPI record creation input."""

    patient_id = serializers.UUIDField()
    enterprise_identifier = serializers.CharField(max_length=100)
    source_system = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    source_patient_identifier = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    demographics_snapshot = serializers.DictField(required=False)


class MPIUpdateSerializer(serializers.Serializer):
    """Validate mutable MPI metadata."""

    source_system = serializers.CharField(max_length=100, required=False)
    source_patient_identifier = serializers.CharField(max_length=150, required=False)
    demographics_snapshot = serializers.DictField(required=False)
    match_score = serializers.DecimalField(
        max_digits=5, decimal_places=4, required=False
    )
    confidence = serializers.DecimalField(
        max_digits=5, decimal_places=4, required=False
    )


class MPILifecycleSerializer(serializers.Serializer):
    """Validate MPI lifecycle requests."""

    status = serializers.CharField(max_length=20)


class MPICandidateSerializer(serializers.ModelSerializer):
    """Serialize MPI candidate matches."""

    class Meta:
        """Serializer metadata."""

        model = MPIMatchCandidate
        fields = (
            "id",
            "left_record",
            "right_record",
            "score",
            "status",
            "evidence",
            "reviewed_at",
            "reviewed_by_id",
            "created_at",
        )
        read_only_fields = fields


class MPIMatchCreateSerializer(serializers.Serializer):
    """Validate MPI candidate generation input."""

    left_record_id = serializers.UUIDField()
    right_record_id = serializers.UUIDField()


class MPIReviewSerializer(serializers.Serializer):
    """Validate candidate review input."""

    status = serializers.ChoiceField(
        choices=("CONFIRMED", "REJECTED"),
    )


class MPIMergeSerializer(serializers.Serializer):
    """Validate MPI merge input."""

    survivor_id = serializers.UUIDField()
    duplicate_id = serializers.UUIDField()
    candidate_id = serializers.UUIDField()


__all__ = (
    "MPICandidateSerializer",
    "MPICreateSerializer",
    "MPIDetailSerializer",
    "MPILifecycleSerializer",
    "MPIListSerializer",
    "MPIMatchCreateSerializer",
    "MPIMergeSerializer",
    "MPIReviewSerializer",
    "MPIUpdateSerializer",
)
