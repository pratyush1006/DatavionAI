"""
Serializers for the Medical History module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "history_type",
    "title",
    "description",
    "clinical_status",
    "onset_date",
    "resolved_date",
    "relationship",
    "is_smoker",
    "alcohol_use",
    "recorded_by",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "history_type",
    "title",
    "description",
    "clinical_status",
    "onset_date",
    "resolved_date",
    "relationship",
    "is_smoker",
    "alcohol_use",
    "recorded_by",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "history_type",
    "title",
    "clinical_status",
    "onset_date",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicalHistory
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientMedicalHistoryCreateSerializer(
    PatientMedicalHistorySerializer,
):
    class Meta(PatientMedicalHistorySerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientMedicalHistoryUpdateSerializer(
    PatientMedicalHistorySerializer,
):
    class Meta(PatientMedicalHistorySerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientMedicalHistoryListSerializer(
    PatientMedicalHistorySerializer,
):
    class Meta(PatientMedicalHistorySerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PatientMedicalHistoryDetailSerializer = PatientMedicalHistorySerializer


__all__ = [
    "PatientMedicalHistoryCreateSerializer",
    "PatientMedicalHistoryDetailSerializer",
    "PatientMedicalHistoryListSerializer",
    "PatientMedicalHistorySerializer",
    "PatientMedicalHistoryUpdateSerializer",
]
