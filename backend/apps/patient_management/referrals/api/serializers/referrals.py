"""
Serializers for the Referrals module.
"""

from __future__ import annotations

from apps.patient_management.referrals.models import PatientReferral
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "referral_number",
    "referring_provider",
    "referred_to",
    "referred_to_organization",
    "reason",
    "priority",
    "urgency",
    "status",
    "clinical_notes",
    "requested_date",
    "appointment_date",
    "completed_date",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "referral_number",
    "referring_provider",
    "referred_to",
    "referred_to_organization",
    "reason",
    "priority",
    "urgency",
    "status",
    "clinical_notes",
    "requested_date",
    "appointment_date",
    "completed_date",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "referral_number",
    "referred_to",
    "priority",
    "urgency",
    "status",
    "requested_date",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class PatientReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReferral
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientReferralCreateSerializer(PatientReferralSerializer):
    class Meta(PatientReferralSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientReferralUpdateSerializer(PatientReferralSerializer):
    class Meta(PatientReferralSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientReferralListSerializer(PatientReferralSerializer):
    class Meta(PatientReferralSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PatientReferralDetailSerializer = PatientReferralSerializer


__all__ = [
    "PatientReferralCreateSerializer",
    "PatientReferralDetailSerializer",
    "PatientReferralListSerializer",
    "PatientReferralSerializer",
    "PatientReferralUpdateSerializer",
]
